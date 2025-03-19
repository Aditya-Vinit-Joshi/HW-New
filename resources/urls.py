from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('', views.home, name='home'),
    path('resources/', views.resource_list, name='resource_list'),
    path('resources/<int:pk>/', views.resource_detail, name='resource_detail'),
    path('resources/create/', views.resource_create, name='resource_create'),
    path('resources/<int:pk>/edit/', views.resource_edit, name='resource_edit'),
    path('resources/<int:pk>/delete/', views.resource_delete, name='resource_delete'),
    path('resources/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('resources/<int:pk>/rate/', views.rate_resource, name='rate_resource'),
    path('resources/<int:pk>/like/', views.like_resource, name='like_resource'),
    path('resources/<int:pk>/save/', views.save_resource, name='save_resource'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('my-resources/', views.my_resources, name='my_resources'),
    path('saved-resources/', views.saved_resources, name='saved_resources'),
    # Admin approval URLs
    path('admin/resources/', views.admin_approval, name='admin_approval'),
    path('resources/<int:pk>/approve/', views.approve_resource, name='approve_resource'),
    path('resources/<int:pk>/reject/', views.reject_resource, name='reject_resource'),
] 