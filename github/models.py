from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GitHubRepository(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField()
    stars = models.PositiveIntegerField(default=0)
    forks = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=100, blank=True)
    topics = models.JSONField(default=list)
    last_updated = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    saved_by = models.ManyToManyField(User, related_name='saved_repos', blank=True)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "GitHub repositories"
    
    def __str__(self):
        return self.name

class RepositoryComment(models.Model):
    repository = models.ForeignKey(GitHubRepository, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Comment by {self.user.username} on {self.repository.name}'

class RepositoryRating(models.Model):
    repository = models.ForeignKey(GitHubRepository, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['repository', 'user']
    
    def __str__(self):
        return f'Rating {self.rating} by {self.user.username} on {self.repository.name}'
