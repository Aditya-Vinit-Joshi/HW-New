from django.shortcuts import render, redirect
from django.db.models import Q
from resources.models import Resource
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Create your views here.

def search_view(request):
    query = request.GET.get('q', '')
    if query:
        # Updated search fields to match the Resource model
        resources = Resource.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        resources = Resource.objects.none()

    context = {
        'query': query,
        'resources': resources,
    }
    return render(request, 'search/search_results.html', context)

def advanced_search(request):
    # Redirect to resources list instead of showing advanced search
    return redirect('resources:resource_list')

def search_results(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    tags = request.GET.getlist('tags')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    sort_by = request.GET.get('sort', '-created_at')
    
    resources = Resource.objects.all()
    
    if query:
        vector = SearchVector('title', weight='A') + \
                 SearchVector('description', weight='B') + \
                 SearchVector('content', weight='C')
        search_query = SearchQuery(query)
        resources = resources.annotate(rank=SearchRank(vector, search_query)) \
                           .filter(rank__gte=0.1) \
                           .order_by('-rank')
    
    if category:
        resources = resources.filter(category=category)
    
    if tags:
        resources = resources.filter(tags__name__in=tags)
    
    if date_from:
        resources = resources.filter(created_at__gte=date_from)
    
    if date_to:
        resources = resources.filter(created_at__lte=date_to)
    
    resources = resources.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(resources, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'category': category,
        'tags': tags,
        'date_from': date_from,
        'date_to': date_to,
        'sort_by': sort_by,
        'page_obj': page_obj,
        'total_results': resources.count(),
    }
    
    return render(request, 'search/search_results.html', context)

@require_GET
def get_suggestions(request):
    query = request.GET.get('q', '').strip()
    suggestions = []
    
    if query:
        # Get title suggestions
        title_suggestions = Resource.objects.filter(
            title__icontains=query
        ).values_list('title', flat=True)[:5]
        
        # Get tag suggestions
        tag_suggestions = Resource.objects.filter(
            tags__name__icontains=query
        ).values_list('tags__name', flat=True).distinct()[:5]
        
        suggestions = list(title_suggestions) + list(tag_suggestions)
        suggestions = list(set(suggestions))[:10]  # Remove duplicates and limit to 10
    
    return JsonResponse({'suggestions': suggestions})
