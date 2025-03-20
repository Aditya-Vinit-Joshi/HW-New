from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator

from django.db.models import Avg, Q, Count
from .models import Resource, Category, Comment, Rating, VideoResource
from .forms import ResourceForm, CommentForm, RatingForm
from django.http import JsonResponse

def is_admin(user):
    return user.is_staff or user.is_superuser

def home(request):
    featured_resources = Resource.objects.filter(is_approved=True).order_by('-views')[:6]
    categories = Category.objects.filter(name__in=['Artificial Intelligence', 'Machine Learning'])
    latest_resources = Resource.objects.filter(is_approved=True).order_by('-created_at')[:6]
    
    context = {
        'featured_resources': featured_resources,
        'categories': categories,
        'latest_resources': latest_resources,
    }
    return render(request, 'resources/home.html', context)

def resource_list(request):
    resources = Resource.objects.filter(is_approved=True)
    
    # Filter by resource type
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        resources = resources.filter(category_id=category_id)
        
    # Filter by search query
    query = request.GET.get('q')
    if query:
        resources = resources.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    
    # Sort resources
    sort_by = request.GET.get('sort', '-created_at')
    valid_sort_fields = {
        'created_at': 'created_at',
        '-created_at': '-created_at',
        'views': 'views',
        '-views': '-views',
        'title': 'title',
        '-title': '-title',
        'rating': 'avg_rating',
        '-rating': '-avg_rating'
    }
    
    # Annotate average rating for all resources
    resources = resources.annotate(avg_rating=Avg('ratings__rating'))
    
    if sort_by in valid_sort_fields:
        resources = resources.order_by(valid_sort_fields[sort_by])
    
    # Pagination
    paginator = Paginator(resources, 12)  # Show 12 resources per page
    page = request.GET.get('page', 1)
    try:
        resources = paginator.page(page)
    except:
        resources = paginator.page(1)
    
    # Get only AI and ML categories for the filter form
    categories = Category.objects.filter(name__in=['Artificial Intelligence', 'Machine Learning'])
    
    # Get all resource types except github
    resource_types = [rt for rt in Resource.RESOURCE_TYPES if rt[0] != 'github']
    
    context = {
        'resources': resources,
        'categories': categories,
        'resource_types': resource_types,
        'current_type': resource_type,
        'current_category': category_id,
        'current_sort': sort_by,
        'query': query,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': resources,
    }
    return render(request, 'resources/resource_list.html', context)

def resource_detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    
    # Increment view count
    resource.views += 1
    resource.save(update_fields=['views'])
    
    # Get comments and ratings
    comments = resource.comments.all().order_by('-created_at')
    ratings = resource.ratings.all()
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    
    # Check if the user has already rated the resource
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = Rating.objects.get(resource=resource, user=request.user)
        except Rating.DoesNotExist:
            pass
    
    # Show pending resources only to staff or the author
    if not resource.is_approved and (request.user != resource.author and not request.user.is_staff):
        messages.warning(request, 'This resource is pending approval and is not publicly available yet.')
        return redirect('resources:resource_list')
    
    context = {
        'resource': resource,
        'comments': comments,
        'comment_form': CommentForm(),
        'rating_form': RatingForm(),
        'avg_rating': avg_rating,
        'user_rating': user_rating,
        'is_liked': request.user in resource.likes.all() if request.user.is_authenticated else False,
        'is_saved': resource in request.user.saved_resources.all() if request.user.is_authenticated else False,
    }
    return render(request, 'resources/resource_detail.html', context)

@login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = request.user
            # Explicitly set approval status - new resources need admin review
            resource.is_approved = False
            resource.is_rejected = False
            resource.save()
            form.save_m2m()  # Save tags
            messages.success(request, 'Resource submitted successfully! It will be reviewed by moderators.')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm()
    
    return render(request, 'resources/resource_form.html', {'form': form, 'action': 'Create'})

@login_required
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    
    if request.user != resource.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this resource.')
        return redirect('resources:resource_detail', pk=pk)
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            resource = form.save()
            messages.success(request, 'Resource updated successfully!')
            return redirect('resources:resource_detail', pk=resource.pk)
    else:
        form = ResourceForm(instance=resource)
    
    return render(request, 'resources/resource_form.html', {'form': form, 'action': 'Edit'})

@login_required
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    
    if request.user != resource.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this resource.')
        return redirect('resources:resource_detail', pk=pk)
    
    if request.method == 'POST':
        resource.delete()
        messages.success(request, 'Resource deleted successfully!')
        return redirect('resources:resource_list')
    
    return render(request, 'resources/resource_confirm_delete.html', {'resource': resource})

@login_required
def add_comment(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.resource = resource
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('resources:resource_detail', pk=pk)

@login_required
def rate_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = Rating.objects.get_or_create(
                resource=resource,
                user=request.user,
                defaults={'rating': form.cleaned_data['rating']}
            )
            if not created:
                rating.rating = form.cleaned_data['rating']
                rating.save()
            messages.success(request, 'Rating submitted successfully!')
        else:
            messages.error(request, 'Error submitting rating.')
    
    return redirect('resources:resource_detail', pk=pk)

@login_required
def like_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    
    if request.user in resource.likes.all():
        resource.likes.remove(request.user)
        liked = False
    else:
        resource.likes.add(request.user)
        liked = True
    
    return JsonResponse({'liked': liked, 'count': resource.likes.count()})

@login_required
def save_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    
    if resource in request.user.saved_resources.all():
        request.user.saved_resources.remove(resource)
        saved = False
    else:
        request.user.saved_resources.add(resource)
        saved = True
    
    return JsonResponse({'saved': saved})

def category_list(request):
    categories = Category.objects.filter(name__in=['Artificial Intelligence', 'Machine Learning'])
    return render(request, 'resources/category_list.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    resources = Resource.objects.filter(category=category, is_approved=True)
    
    # Filter by resource type
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(resource_type=resource_type)
    
    # Sort resources
    sort_by = request.GET.get('sort', '-created_at')
    resources = resources.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(resources, 12)
    page = request.GET.get('page')
    resources = paginator.get_page(page)
    
    context = {
        'category': category,
        'resources': resources,
        'resource_types': Resource.RESOURCE_TYPES,
        'sort_by': sort_by,
    }
    return render(request, 'resources/category_detail.html', context)

@login_required
def my_resources(request):
    resources = Resource.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'resources/my_resources.html', {'resources': resources})

@login_required
def saved_resources(request):
    saved_resources = request.user.saved_resources.all()
    saved_videos = request.user.saved_video_resources.all()
    
    context = {
        'saved_resources': saved_resources,
        'saved_videos': saved_videos,
    }
    return render(request, 'resources/saved_resources.html', context)


@user_passes_test(is_admin)
def admin_approval(request):
    # Count resources by status
    pending_count = Resource.objects.filter(is_approved=False, is_rejected=False).count()
    approved_count = Resource.objects.filter(is_approved=True).count()
    rejected_count = Resource.objects.filter(is_rejected=True).count()
    total_count = Resource.objects.count()
    
    # Check if JSON format is requested (for admin dashboard)
    if request.GET.get('format') == 'json':
        return JsonResponse({
            'pending_count': pending_count,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
            'total_count': total_count,
        })
    
    filter_type = request.GET.get('filter', 'pending')
    
    if filter_type == 'pending':
        resources = Resource.objects.filter(is_approved=False, is_rejected=False)
        filter_message = "Showing pending resources awaiting review"
    elif filter_type == 'approved':
        resources = Resource.objects.filter(is_approved=True)
        filter_message = "Showing approved resources"
    elif filter_type == 'rejected':
        resources = Resource.objects.filter(is_rejected=True)
        filter_message = "Showing rejected resources"
    else:  # 'all' filter or any other value
        resources = Resource.objects.all()
        filter_message = "Showing all resources"
    
    # Sort by newest first
    resources = resources.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(resources, 20)  # Show 20 resources per page
    page = request.GET.get('page', 1)
    try:
        resources = paginator.page(page)
    except:
        resources = paginator.page(1)
    
    context = {
        'resources': resources,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'total_count': total_count,
        'filter': filter_type,
        'filter_message': filter_message,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': resources,
    }
    return render(request, 'resources/admin_approval.html', context)

@user_passes_test(is_admin)
def approve_resource(request, pk):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, pk=pk)
        resource.is_approved = True
        resource.is_rejected = False
        resource.save()
        messages.success(request, f'Resource "{resource.title}" has been approved.')
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@user_passes_test(is_admin)
def reject_resource(request, pk):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, pk=pk)
        resource.is_approved = False
        resource.is_rejected = True
        resource.save()
        messages.success(request, f'Resource "{resource.title}" has been rejected.')
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def video_resources(request):
    videos = VideoResource.objects.filter(is_approved=True)
    
    # Filter by platform
    platform = request.GET.get('platform')
    if platform:
        videos = videos.filter(platform=platform)
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        videos = videos.filter(category_id=category_id)
        
    # Filter by search query
    query = request.GET.get('q')
    if query:
        videos = videos.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(instructor__icontains=query)
        ).distinct()
    
    # Sort videos
    sort_by = request.GET.get('sort', '-created_at')
    videos = videos.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(videos, 12)  # Show 12 videos per page
    page = request.GET.get('page', 1)
    try:
        videos = paginator.page(page)
    except:
        videos = paginator.page(1)
    
    # Get only AI and ML categories for the filter form
    categories = Category.objects.filter(name__in=['Artificial Intelligence', 'Machine Learning'])
    
    context = {
        'videos': videos,
        'categories': categories,
        'platforms': VideoResource.PLATFORMS,
        'current_platform': platform,
        'current_category': category_id,
        'current_sort': sort_by,
        'query': query,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': videos,
    }
    return render(request, 'resources/video_resources.html', context)

@login_required
def like_video(request, video_id):
    video = get_object_or_404(VideoResource, pk=video_id)
    
    if request.user in video.likes.all():
        video.likes.remove(request.user)
        liked = False
    else:
        video.likes.add(request.user)
        liked = True
    
    return JsonResponse({'liked': liked, 'count': video.likes.count()})

def video_resource_detail(request, pk):
    video = get_object_or_404(VideoResource, pk=pk)
    
    # Increment view count
    video.views += 1
    video.save(update_fields=['views'])
    
    # Show pending videos only to staff or the author
    if not video.is_approved and (request.user != video.author and not request.user.is_staff):
        messages.warning(request, 'This video is pending approval and is not publicly available yet.')
        return redirect('resources:video_list')
    
    context = {
        'video': video,
        'is_liked': request.user in video.likes.all() if request.user.is_authenticated else False,
        'is_saved': video in request.user.saved_video_resources.all() if request.user.is_authenticated else False,
    }
    return render(request, 'resources/video_detail.html', context)

@login_required
def save_video_resource(request, pk):
    video = get_object_or_404(VideoResource, pk=pk)
    
    if video in request.user.saved_video_resources.all():
        request.user.saved_video_resources.remove(video)
        saved = False
    else:
        request.user.saved_video_resources.add(video)
        saved = True
    
    return JsonResponse({'saved': saved})

