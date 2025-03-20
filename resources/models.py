from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name

class Resource(models.Model):
    RESOURCE_TYPES = [
        ('tutorial', 'Tutorial'),
        ('course', 'Course'),
        ('documentation', 'Documentation'),
        ('research', 'Research Paper'),
        ('github', 'GitHub Repository'),
        ('blog', 'Blog Post'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='resources')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_resources', blank=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.resource.title}'

class Rating(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['resource', 'user']
    
    def __str__(self):
        return f'Rating {self.rating} by {self.user.username} on {self.resource.title}'

class VideoResource(models.Model):
    PLATFORMS = [
        ('youtube', 'YouTube'),
        ('coursera', 'Coursera'),
        ('udemy', 'Udemy'),
        ('edx', 'edX'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    platform = models.CharField(max_length=20, choices=PLATFORMS)
    thumbnail_url = models.URLField(blank=True, null=True)
    duration = models.CharField(max_length=50, blank=True, null=True)  # e.g., "2h 30m"
    instructor = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='video_resources')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
