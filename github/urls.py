from django.urls import path
from . import views

app_name = 'github'

urlpatterns = [
    path('', views.github_repos, name='repos'),
    path('trending/', views.trending_repos, name='trending'),
    path('repo/<int:pk>/', views.repo_detail, name='repo_detail'),
    path('repo/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('repo/<int:pk>/rate/', views.rate_repo, name='rate_repo'),
    path('repo/<int:pk>/save/', views.save_repo, name='save_repo'),
    path('saved-repos/', views.saved_repos, name='saved_repos'),
    path('sync-repos/', views.sync_repos, name='sync_repos'),
] 