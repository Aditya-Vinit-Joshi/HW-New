from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resources.models import VideoResource, Category
from taggit.models import Tag

User = get_user_model()

class Command(BaseCommand):
    help = 'Add AI/ML related YouTube videos'

    def handle(self, *args, **kwargs):
        # Ensure we have an admin user
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )

        # Ensure we have AI and ML categories
        ai_category, _ = Category.objects.get_or_create(
            name='Artificial Intelligence',
            defaults={'description': 'Resources about Artificial Intelligence', 'slug': 'artificial-intelligence'}
        )
        ml_category, _ = Category.objects.get_or_create(
            name='Machine Learning',
            defaults={'description': 'Resources about Machine Learning', 'slug': 'machine-learning'}
        )

        # List of AI/ML YouTube videos
        videos = [
            {
                'title': 'Neural Networks from Scratch',
                'description': 'Learn how to build neural networks from the ground up',
                'url': 'https://www.youtube.com/watch?v=Wo5dMEP_BbI',
                'thumbnail_url': 'https://img.youtube.com/vi/Wo5dMEP_BbI/maxresdefault.jpg',
                'duration': '1h 30m',
                'instructor': 'Sentdex',
                'category': ml_category,
                'tags': ['neural networks', 'python', 'deep learning'],
            },
            {
                'title': 'Introduction to Machine Learning',
                'description': 'A comprehensive introduction to machine learning concepts',
                'url': 'https://www.youtube.com/watch?v=PPLop4L2eGk',
                'thumbnail_url': 'https://img.youtube.com/vi/PPLop4L2eGk/maxresdefault.jpg',
                'duration': '2h',
                'instructor': 'Andrew Ng',
                'category': ml_category,
                'tags': ['machine learning', 'basics', 'algorithms'],
            },
            # Add more videos here...
            {
                'title': 'Deep Learning Fundamentals',
                'description': 'Understanding the basics of deep learning',
                'url': 'https://www.youtube.com/watch?v=aircAruvnKk',
                'thumbnail_url': 'https://img.youtube.com/vi/aircAruvnKk/maxresdefault.jpg',
                'duration': '45m',
                'instructor': '3Blue1Brown',
                'category': ml_category,
                'tags': ['deep learning', 'neural networks', 'mathematics'],
            },
            # Add more videos...
        ]

        # Add videos to database
        for video_data in videos:
            tags = video_data.pop('tags')
            video, created = VideoResource.objects.get_or_create(
                url=video_data['url'],
                defaults={
                    **video_data,
                    'platform': 'youtube',
                    'is_approved': True,
                }
            )
            if created:
                video.tags.add(*tags)
                self.stdout.write(self.style.SUCCESS(f'Added video: {video.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Video already exists: {video.title}')) 