from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.core.paginator import Paginator
from .models import GitHubRepository, RepositoryComment, RepositoryRating
from .forms import CommentForm, RatingForm
import requests
import datetime

def github_repos(request):
    base_url = "https://api.github.com/search/repositories"
    params = {
        "q": "machine+learning+OR+artificial+intelligence+OR+deep+learning+OR+generative+ai",
        "sort": "stars",
        "order": "desc",
        "per_page": 100,
    }

    # Process filters from the request
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    sort_by = request.GET.get('sort', 'stars')

    if query:
        params["q"] += f"+{query}"

    if category:
        params["q"] += f"+category:{category}"

    # Filter by date range if present
    if date_from and date_to:
        params["q"] += f"+created:{date_from}..{date_to}"

    params['sort'] = sort_by  # Update sort parameter

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        if 'items' not in data:
            # If API call fails, fall back to database
            repos = GitHubRepository.objects.all().order_by('-stars')
        else:
            repos = data['items']
            
    except (requests.RequestException, KeyError) as e:
        # If there's any error, fall back to database
        repos = GitHubRepository.objects.all().order_by('-stars')
        messages.warning(request, 'Unable to fetch from GitHub API. Showing cached repositories.')

    # Paginate the results
    paginator = Paginator(repos, 12)
    page = request.GET.get('page')
    repos = paginator.get_page(page)

    context = {
        'repos': repos,
        'query': query,
        'category': category,
        'date_from': date_from,
        'date_to': date_to,
        'sort_by': sort_by,
    }
    return render(request, 'github/repo_list.html', context)

def trending_repos(request):
    language = request.GET.get('language', '')
    time_period = request.GET.get('time', 'daily')  # daily, weekly, monthly
    
    repos = GitHubRepository.objects.all()
    
    if language:
        repos = repos.filter(language__iexact=language)
    
    # Filter by time period
    if time_period == 'daily':
        since = datetime.datetime.now() - datetime.timedelta(days=1)
    elif time_period == 'weekly':
        since = datetime.datetime.now() - datetime.timedelta(weeks=1)
    else:
        since = datetime.datetime.now() - datetime.timedelta(days=30)
    
    repos = repos.filter(created_at__gte=since).order_by('-stars')
    
    paginator = Paginator(repos, 12)
    page = request.GET.get('page')
    repos = paginator.get_page(page)
    
    languages = GitHubRepository.objects.values_list('language', flat=True).distinct()
    
    context = {
        'repos': repos,
        'languages': languages,
        'selected_language': language,
        'time_period': time_period,
    }
    return render(request, 'github/trending.html', context)

def repo_detail(request, pk):
    repo = get_object_or_404(GitHubRepository, pk=pk)
    comments = repo.comments.all().order_by('-created_at')
    rating_form = RatingForm()
    comment_form = CommentForm()
    
    # Get average rating
    avg_rating = repo.ratings.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'repo': repo,
        'comments': comments,
        'rating_form': rating_form,
        'comment_form': comment_form,
        'avg_rating': avg_rating,
    }
    return render(request, 'github/repo_detail.html', context)

@login_required
def add_comment(request, pk):
    repo = get_object_or_404(GitHubRepository, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.repository = repo
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('github:repo_detail', pk=pk)

@login_required
def rate_repo(request, pk):
    repo = get_object_or_404(GitHubRepository, pk=pk)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating, created = RepositoryRating.objects.get_or_create(
                repository=repo,
                user=request.user,
                defaults={'rating': form.cleaned_data['rating']}
            )
            if not created:
                rating.rating = form.cleaned_data['rating']
                rating.save()
            messages.success(request, 'Rating submitted successfully!')
        else:
            messages.error(request, 'Error submitting rating.')
    
    return redirect('github:repo_detail', pk=pk)

@login_required
def save_repo(request, pk):
    repo = get_object_or_404(GitHubRepository, pk=pk)
    
    if request.user in repo.saved_by.all():
        repo.saved_by.remove(request.user)
        saved = False
    else:
        repo.saved_by.add(request.user)
        saved = True
    
    return JsonResponse({'saved': saved})

@login_required
def saved_repos(request):
    repos = request.user.saved_repos.all().order_by('-stars')
    return render(request, 'github/saved_repos.html', {'repos': repos})

@login_required
def sync_repos(request):
    if not settings.GITHUB_TOKEN:
        messages.error(request, 'GitHub token not configured.')
        return redirect('github:repos')
    
    headers = {
        'Authorization': f'token {settings.GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    try:
        # Get trending AI repositories
        response = requests.get(
            'https://api.github.com/search/repositories',
            headers=headers,
            params={
                'q': 'topic:artificial-intelligence',
                'sort': 'stars',
                'order': 'desc',
            }
        )
        response.raise_for_status()
        
        for item in response.json()['items']:
            repo, created = GitHubRepository.objects.update_or_create(
                name=item['name'],
                defaults={
                    'description': item['description'] or '',
                    'url': item['html_url'],
                    'stars': item['stargazers_count'],
                    'forks': item['forks_count'],
                    'language': item['language'] or '',
                    'topics': item.get('topics', []),
                    'last_updated': datetime.datetime.strptime(
                        item['updated_at'], '%Y-%m-%dT%H:%M:%SZ'
                    ),
                }
            )
        
        messages.success(request, 'Repositories synchronized successfully!')
    except Exception as e:
        messages.error(request, f'Error synchronizing repositories: {str(e)}')
    
    return redirect('github:repos')
