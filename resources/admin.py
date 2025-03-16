from django.contrib import admin
from .models import Resource, Category, Comment, Rating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'category', 'author', 'created_at', 'is_approved')
    list_filter = ('resource_type', 'category', 'is_approved', 'created_at')
    search_fields = ('title', 'description')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('resource', 'author', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'resource__title')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'resource__title')
