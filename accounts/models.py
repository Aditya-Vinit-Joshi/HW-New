from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    interests = models.ManyToManyField('resources.Category', related_name='interested_users', blank=True)
    saved_resources = models.ManyToManyField('resources.Resource', related_name='saved_by_users', blank=True)
    saved_video_resources = models.ManyToManyField('resources.VideoResource', related_name='saved_by_users', blank=True)
    
    def __str__(self):
        return self.username
