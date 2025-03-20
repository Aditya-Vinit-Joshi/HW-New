from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator

from django.db.models import Avg, Q, Count
from .models import Resource, Category, Comment, Rating
from django.db.models import Avg, Q
from .models import Resource, Category, Comment, Rating, VideoResource

from .forms import ResourceForm, CommentForm, RatingForm
from django.http import JsonResponse

def is_admin(user):
    return user.is_staff or user.is_superuser

def home(request):
    featured_resources = Resource.objects.filter(is_approved=True).order_by('-views')[:6]
    categories = Category.objects.all()
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
    
    # Get all categories and resource types for the filter form
    categories = Category.objects.all()
    
    context = {
        'resources': resources,
        'categories': categories,
        'resource_types': Resource.RESOURCE_TYPES,
        'current_type': resource_type,
        'current_category': category_id,
        'current_sort': sort_by,
        'query': query,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': resources,
    }
    return render(request, 'resources/resource_list.html', context)

def resource_detail(request, pk):
    return render(request, pk)

@login_required
def resource_create(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.author = request.user
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
    categories = Category.objects.all()
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
    resources = request.user.saved_resources.all().order_by('-created_at')
    return render(request, 'resources/saved_resources.html', {'resources': resources})


@user_passes_test(is_admin)
def admin_approval(request):
    filter_type = request.GET.get('filter', 'pending')
    
    if filter_type == 'pending':
        resources = Resource.objects.filter(is_approved=False, is_rejected=False)
    elif filter_type == 'approved':
        resources = Resource.objects.filter(is_approved=True)
    elif filter_type == 'rejected':
        resources = Resource.objects.filter(is_rejected=True)
    else:
        resources = Resource.objects.all()
    
    resources = resources.order_by('-created_at')
    
    # Count pending resources
    pending_count = Resource.objects.filter(is_approved=False, is_rejected=False).count()
    
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
        'filter': filter_type,
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

def video_resources(request):
    # Get filter parameters
    platform = request.GET.get('platform', '')
    category = request.GET.get('category', '')
    search_query = request.GET.get('q', '')
    
    # Start with all approved video resources
    videos = VideoResource.objects.filter(is_approved=True)
    
    # Apply filters
    if platform:
        videos = videos.filter(platform=platform)
    if category:
        videos = videos.filter(category__slug=category)
    if search_query:
        videos = videos.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Get all categories for the filter dropdown
    categories = Category.objects.all()
    
    # Get unique platforms for the filter dropdown
    platforms = VideoResource.PLATFORMS
    
    # Paginate results
    paginator = Paginator(videos, 12)  # Show 12 videos per page
    page = request.GET.get('page')
    videos = paginator.get_page(page)
    
    context = {
        'videos': videos,
        'categories': categories,
        'platforms': platforms,
        'selected_platform': platform,
        'selected_category': category,
        'search_query': search_query,
    }
    
    return render(request, 'resources/video_resources.html', context)

@login_required
def like_video(request, video_id):
    video = get_object_or_404(VideoResource, id=video_id)
    
    if request.user in video.likes.all():
        video.likes.remove(request.user)
        liked = False
    else:
        video.likes.add(request.user)
        liked = True
    
    return JsonResponse({'liked': liked})

