from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resources.models import VideoResource, Category
from taggit.models import Tag
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = 'Generates 1000+ video resources for AI/ML learning'

    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Get or create categories
        categories = {
            'machine-learning': {
                'name': 'Machine Learning',
                'description': 'Resources related to machine learning algorithms, techniques, and applications',
                'subcategories': ['supervised learning', 'unsupervised learning', 'reinforcement learning', 'deep learning']
            },
            'artificial-intelligence': {
                'name': 'Artificial Intelligence',
                'description': 'Resources about AI theory, applications, and ethics',
                'subcategories': ['computer vision', 'natural language processing', 'robotics', 'expert systems']
            },
            'data-science': {
                'name': 'Data Science',
                'description': 'Resources for data analysis, visualization, and processing',
                'subcategories': ['data analysis', 'data visualization', 'big data', 'statistics']
            },
            'computer-vision': {
                'name': 'Computer Vision',
                'description': 'Resources about image and video processing, object detection, and recognition',
                'subcategories': ['image processing', 'object detection', 'face recognition', 'video analysis']
            },
            'nlp': {
                'name': 'Natural Language Processing',
                'description': 'Resources about text processing, language models, and NLP applications',
                'subcategories': ['text processing', 'language models', 'sentiment analysis', 'machine translation']
            }
        }

        # Create categories
        created_categories = {}
        for slug, data in categories.items():
            category, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': data['name'],
                    'description': data['description']
                }
            )
            created_categories[slug] = category

        # Platforms and their characteristics
        platforms = {
            'youtube': {
                'duration_formats': ['10:00', '15:30', '20:45', '30:00', '45:00', '1:00:00'],
                'instructor_prefixes': ['Dr.', 'Prof.', 'Mr.', 'Ms.', ''],
                'thumbnail_urls': [
                    'https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg',
                    'https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg',
                    'https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg'
                ]
            },
            'coursera': {
                'duration_formats': ['4 weeks', '6 weeks', '8 weeks', '12 weeks', '16 weeks'],
                'instructor_prefixes': ['Dr.', 'Prof.', 'Associate Prof.', ''],
                'thumbnail_urls': [
                    'https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera-course-photos.s3.amazonaws.com/83/e258e0532611e5a5382b9d91fefd6b/jhepburn_course_image.png'
                ]
            },
            'udemy': {
                'duration_formats': ['2 hours', '4 hours', '6 hours', '8 hours', '10 hours', '12 hours'],
                'instructor_prefixes': ['Dr.', 'Mr.', 'Ms.', ''],
                'thumbnail_urls': [
                    'https://img-c.udemycdn.com/course/480x270/567828_67d0.jpg',
                    'https://img-c.udemycdn.com/course/480x270/1359810_8e6b_2.jpg'
                ]
            },
            'edx': {
                'duration_formats': ['4 weeks', '6 weeks', '8 weeks', '12 weeks'],
                'instructor_prefixes': ['Dr.', 'Prof.', 'Associate Prof.', ''],
                'thumbnail_urls': [
                    'https://prod-discovery.edx-cdn.org/media/course/image/0eccf4d9-ef2c-4c0c-9b70-bb5c0d23d3e5-8372a9aafcda-spt-default.png'
                ]
            }
        }

        # Common tags for each category
        category_tags = {
            'machine-learning': ['machine learning', 'ml', 'deep learning', 'neural networks', 'supervised learning', 'unsupervised learning'],
            'artificial-intelligence': ['ai', 'artificial intelligence', 'robotics', 'expert systems', 'ai ethics'],
            'data-science': ['data science', 'data analysis', 'statistics', 'big data', 'data visualization'],
            'computer-vision': ['computer vision', 'image processing', 'object detection', 'face recognition'],
            'nlp': ['nlp', 'natural language processing', 'text processing', 'language models']
        }

        # Generate 1000+ video resources
        for i in range(1000):
            # Select random category and platform
            category_slug = random.choice(list(categories.keys()))
            category = created_categories[category_slug]
            platform = random.choice(list(platforms.keys()))
            platform_data = platforms[platform]

            # Generate title and description
            subcategory = random.choice(categories[category_slug]['subcategories'])
            title = f"{fake.word().capitalize()} {subcategory}: {fake.sentence(nb_words=4)}"
            description = fake.paragraph(nb_sentences=3)

            # Generate URL based on platform
            if platform == 'youtube':
                url = f"https://www.youtube.com/watch?v={fake.uuid4()[:11]}"
            elif platform == 'coursera':
                url = f"https://www.coursera.org/learn/{fake.slug()}"
            elif platform == 'udemy':
                url = f"https://www.udemy.com/course/{fake.slug()}"
            else:  # edx
                url = f"https://www.edx.org/course/{fake.slug()}"

            # Generate instructor name
            prefix = random.choice(platform_data['instructor_prefixes'])
            instructor = f"{prefix} {fake.name()}"

            # Generate duration
            duration = random.choice(platform_data['duration_formats'])

            # Select thumbnail
            thumbnail_url = random.choice(platform_data['thumbnail_urls'])

            # Generate tags
            base_tags = category_tags[category_slug]
            additional_tags = random.sample(base_tags, random.randint(2, 4))
            tags = additional_tags + [platform]

            # Create video resource
            video_data = {
                'title': title,
                'description': description,
                'url': url,
                'platform': platform,
                'thumbnail_url': thumbnail_url,
                'duration': duration,
                'instructor': instructor,
                'category': category,
                'is_approved': True
            }

            video, created = VideoResource.objects.get_or_create(
                title=title,
                defaults=video_data
            )

            # Add tags
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                video.tags.add(tag)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created video {i+1}/1000: {title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated video {i+1}/1000: {title}'))

        self.stdout.write(self.style.SUCCESS('Successfully generated 1000+ video resources')) 