from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_view, name='search'),
    path('advanced/', views.advanced_search, name='advanced_search'),
    path('results/', views.search_results, name='search_results'),
    path('suggestions/', views.get_suggestions, name='get_suggestions'),
] 