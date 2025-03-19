from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resources.models import VideoResource, Category
from taggit.models import Tag

User = get_user_model()

class Command(BaseCommand):
    help = 'Loads initial video resources for AI/ML learning'

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
        ml_category, _ = Category.objects.get_or_create(
            slug='machine-learning',
            defaults={
                'name': 'Machine Learning',
                'description': 'Resources related to machine learning algorithms, techniques, and applications'
            }
        )

        ai_category, _ = Category.objects.get_or_create(
            slug='artificial-intelligence',
            defaults={
                'name': 'Artificial Intelligence',
                'description': 'Resources about AI theory, applications, and ethics'
            }
        )

        # Comprehensive video resources
        videos = [
            # Coursera Courses
            {
                'title': 'Machine Learning Specialization',
                'description': 'A comprehensive introduction to machine learning, data mining, and statistical pattern recognition.',
                'url': 'https://www.coursera.org/specializations/machine-learning-introduction',
                'platform': 'coursera',
                'thumbnail_url': 'https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera-course-photos.s3.amazonaws.com/83/e258e0532611e5a5382b9d91fefd6b/jhepburn_course_image.png',
                'duration': '3 months',
                'instructor': 'Andrew Ng',
                'category': ml_category,
                'tags': ['machine learning', 'deep learning', 'neural networks', 'coursera']
            },
            {
                'title': 'Deep Learning Specialization',
                'description': 'Master Deep Learning, and Break into AI. Learn the foundations of deep learning and get practical experience in building and training neural networks.',
                'url': 'https://www.coursera.org/specializations/deep-learning',
                'platform': 'coursera',
                'thumbnail_url': 'https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera-course-photos.s3.amazonaws.com/83/e258e0532611e5a5382b9d91fefd6b/jhepburn_course_image.png',
                'duration': '5 months',
                'instructor': 'Andrew Ng',
                'category': ml_category,
                'tags': ['deep learning', 'neural networks', 'coursera']
            },
            {
                'title': 'AI for Everyone',
                'description': 'Learn what AI is, how to build AI projects, and how to work with an AI team.',
                'url': 'https://www.coursera.org/learn/ai-for-everyone',
                'platform': 'coursera',
                'thumbnail_url': 'https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera-course-photos.s3.amazonaws.com/83/e258e0532611e5a5382b9d91fefd6b/jhepburn_course_image.png',
                'duration': '4 weeks',
                'instructor': 'Andrew Ng',
                'category': ai_category,
                'tags': ['artificial intelligence', 'business', 'coursera']
            },
            {
                'title': 'Natural Language Processing Specialization',
                'description': 'Design NLP applications that perform question-answering and sentiment analysis.',
                'url': 'https://www.coursera.org/specializations/natural-language-processing',
                'platform': 'coursera',
                'thumbnail_url': 'https://d3njjcbhbojbot.cloudfront.net/api/utilities/v1/imageproxy/https://coursera-course-photos.s3.amazonaws.com/83/e258e0532611e5a5382b9d91fefd6b/jhepburn_course_image.png',
                'duration': '4 months',
                'instructor': 'Younes Bensouda Mourri',
                'category': ai_category,
                'tags': ['nlp', 'natural language processing', 'coursera']
            },

            # Udemy Courses
            {
                'title': 'Python for Data Science and Machine Learning Bootcamp',
                'description': 'Learn how to use NumPy, Pandas, Seaborn, Matplotlib, Plotly, Scikit-Learn, Machine Learning, Tensorflow, and more!',
                'url': 'https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/',
                'platform': 'udemy',
                'thumbnail_url': 'https://img-c.udemycdn.com/course/480x270/567828_67d0.jpg',
                'duration': '44 hours',
                'instructor': 'Jose Portilla',
                'category': ml_category,
                'tags': ['python', 'data science', 'machine learning', 'udemy']
            },
            {
                'title': 'Deep Learning A-Z™: Hands-On Artificial Neural Networks',
                'description': 'Learn to create Deep Learning Algorithms in Python from two Machine Learning & Data Science experts.',
                'url': 'https://www.udemy.com/course/deeplearning/',
                'platform': 'udemy',
                'thumbnail_url': 'https://img-c.udemycdn.com/course/480x270/1359810_8e6b_2.jpg',
                'duration': '44.5 hours',
                'instructor': 'Kirill Eremenko',
                'category': ml_category,
                'tags': ['deep learning', 'neural networks', 'udemy']
            },
            {
                'title': 'Artificial Intelligence A-Z™: Learn How To Build An AI',
                'description': 'Combine the power of Data Science, Machine Learning and Deep Learning to create powerful AI for Real-World applications!',
                'url': 'https://www.udemy.com/course/artificial-intelligence-az/',
                'platform': 'udemy',
                'thumbnail_url': 'https://img-c.udemycdn.com/course/480x270/685010_7727_4.jpg',
                'duration': '44.5 hours',
                'instructor': 'Kirill Eremenko',
                'category': ai_category,
                'tags': ['artificial intelligence', 'machine learning', 'udemy']
            },

            # YouTube Channels/Series
            {
                'title': '3Blue1Brown - Neural Networks',
                'description': 'A series of videos explaining neural networks in an intuitive way.',
                'url': 'https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi',
                'platform': 'youtube',
                'thumbnail_url': 'https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg',
                'duration': 'Series',
                'instructor': 'Grant Sanderson',
                'category': ml_category,
                'tags': ['neural networks', 'deep learning', 'youtube']
            },
            {
                'title': 'Two Minute Papers - AI Research',
                'description': 'Short, accessible explanations of cutting-edge AI research papers.',
                'url': 'https://www.youtube.com/playlist?list=PLujxSBD-JXglGL3ERdDOhthD3ApwDIYPy',
                'platform': 'youtube',
                'thumbnail_url': 'https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg',
                'duration': 'Ongoing Series',
                'instructor': 'Károly Zsolnai-Fehér',
                'category': ai_category,
                'tags': ['ai research', 'papers', 'youtube']
            },
            {
                'title': 'Yannic Kilcher - AI Research Paper Reviews',
                'description': 'In-depth analysis of recent AI research papers.',
                'url': 'https://www.youtube.com/playlist?list=PLtmWHNX-gukIc92m5K0pEU6LZ1ZQl_7X0',
                'platform': 'youtube',
                'thumbnail_url': 'https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg',
                'duration': 'Ongoing Series',
                'instructor': 'Yannic Kilcher',
                'category': ai_category,
                'tags': ['ai research', 'papers', 'youtube']
            },

            # edX Courses
            {
                'title': 'CS50\'s Introduction to Artificial Intelligence with Python',
                'description': 'Learn to use machine learning in Python in this introductory course on artificial intelligence.',
                'url': 'https://www.edx.org/course/cs50s-introduction-to-artificial-intelligence-with-python',
                'platform': 'edx',
                'thumbnail_url': 'https://prod-discovery.edx-cdn.org/media/course/image/0eccf4d9-ef2c-4c0c-9b70-bb5c0d23d3e5-8372a9aafcda-spt-default.png',
                'duration': '7 weeks',
                'instructor': 'David J. Malan',
                'category': ai_category,
                'tags': ['artificial intelligence', 'python', 'edx']
            },
            {
                'title': 'Principles of Machine Learning',
                'description': 'Learn the fundamentals of machine learning and how to use these techniques to build real-world AI applications.',
                'url': 'https://www.edx.org/course/principles-of-machine-learning',
                'platform': 'edx',
                'thumbnail_url': 'https://prod-discovery.edx-cdn.org/media/course/image/0eccf4d9-ef2c-4c0c-9b70-bb5c0d23d3e5-8372a9aafcda-spt-default.png',
                'duration': '6 weeks',
                'instructor': 'Microsoft',
                'category': ml_category,
                'tags': ['machine learning', 'microsoft', 'edx']
            },
            {
                'title': 'Deep Learning Fundamentals',
                'description': 'Learn the fundamentals of deep learning and neural networks.',
                'url': 'https://www.edx.org/course/deep-learning-fundamentals',
                'platform': 'edx',
                'thumbnail_url': 'https://prod-discovery.edx-cdn.org/media/course/image/0eccf4d9-ef2c-4c0c-9b70-bb5c0d23d3e5-8372a9aafcda-spt-default.png',
                'duration': '8 weeks',
                'instructor': 'IBM',
                'category': ml_category,
                'tags': ['deep learning', 'neural networks', 'ibm', 'edx']
            },

            # Additional YouTube Resources
            {
                'title': 'FastAI - Practical Deep Learning for Coders',
                'description': 'A free course designed for people with some coding experience, who want to learn how to apply deep learning and machine learning to practical problems.',
                'url': 'https://www.youtube.com/playlist?list=PLtmWHNX-gukIc92m5K0pEU6LZ1ZQl_7X0',
                'platform': 'youtube',
                'thumbnail_url': 'https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg',
                'duration': 'Course',
                'instructor': 'Jeremy Howard',
                'category': ml_category,
                'tags': ['deep learning', 'fastai', 'practical', 'youtube']
            },
            {
                'title': 'Sentdex - Machine Learning with Python',
                'description': 'A comprehensive series on machine learning using Python, covering everything from basics to advanced topics.',
                'url': 'https://www.youtube.com/playlist?list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v',
                'platform': 'youtube',
                'thumbnail_url': 'https://i.ytimg.com/vi/aircAruvnKk/maxresdefault.jpg',
                'duration': 'Series',
                'instructor': 'Harrison Kinsley',
                'category': ml_category,
                'tags': ['machine learning', 'python', 'tutorials', 'youtube']
            }
        ]

        # Create video resources
        for video_data in videos:
            tags = video_data.pop('tags')
            video, created = VideoResource.objects.get_or_create(
                title=video_data['title'],
                defaults={
                    **video_data,
                    'is_approved': True
                }
            )
            
            # Add tags
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                video.tags.add(tag)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created video: {video.title}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated video: {video.title}')) 