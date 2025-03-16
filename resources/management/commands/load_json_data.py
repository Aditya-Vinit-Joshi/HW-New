import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from resources.models import Resource, Category
from taggit.models import Tag

User = get_user_model()

class Command(BaseCommand):
    help = 'Load data from JSON files into the database'

    def handle(self, *args, **kwargs):
        # Create default categories using get_or_create
        categories = {
            'machine-learning': Category.objects.get_or_create(
                slug='machine-learning',
                defaults={
                    'name': 'Machine Learning',
                    'description': 'Resources related to machine learning algorithms and applications'
                }
            )[0],
            'artificial-intelligence': Category.objects.get_or_create(
                slug='artificial-intelligence',
                defaults={
                    'name': 'Artificial Intelligence',
                    'description': 'Resources about AI theory, applications, and ethics'
                }
            )[0],
            'github': Category.objects.get_or_create(
                slug='github-projects',
                defaults={
                    'name': 'GitHub Projects',
                    'description': 'Notable AI and ML open source projects'
                }
            )[0]
        }

        # Create a default admin user if not exists
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'is_staff': True,
                'is_superuser': True,
                'email': 'admin@example.com'
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()

        try:
            # Load GitHub repositories
            with open('github_ai_repos.json', 'r', encoding='utf-8') as f:
                github_data = json.load(f)
                for repo in github_data:
                    # Check if resource already exists
                    resource, created = Resource.objects.get_or_create(
                        url=repo['html_url'],
                        defaults={
                            'title': repo['name'],
                            'description': repo.get('description', ''),
                            'resource_type': 'github',
                            'category': categories['github'],
                            'author': admin_user,
                            'is_approved': True
                        }
                    )
                    if created:
                        # Add topics as tags
                        for topic in repo.get('topics', []):
                            resource.tags.add(topic)

            # Load AI papers
            with open('papers_Artificial_Intelligence.json', 'r', encoding='utf-8') as f:
                ai_papers = json.load(f)
                for paper in ai_papers:
                    # Check if resource already exists
                    resource, created = Resource.objects.get_or_create(
                        url=paper['url'],
                        defaults={
                            'title': paper['title'],
                            'description': paper['abstract'],
                            'resource_type': 'research',
                            'category': categories['artificial-intelligence'],
                            'author': admin_user,
                            'is_approved': True
                        }
                    )
                    if created and 'Keywords:' in paper['abstract']:
                        keywords = paper['abstract'].split('Keywords:')[1].split(',')
                        for keyword in keywords:
                            resource.tags.add(keyword.strip().lower())

            # Load ML papers
            with open('papers_Machine_Learning.json', 'r', encoding='utf-8') as f:
                ml_papers = json.load(f)
                for paper in ml_papers:
                    # Check if resource already exists
                    resource, created = Resource.objects.get_or_create(
                        url=paper['url'],
                        defaults={
                            'title': paper['title'],
                            'description': paper['abstract'],
                            'resource_type': 'research',
                            'category': categories['machine-learning'],
                            'author': admin_user,
                            'is_approved': True
                        }
                    )
                    if created and 'Keywords:' in paper['abstract']:
                        keywords = paper['abstract'].split('Keywords:')[1].split(',')
                        for keyword in keywords:
                            resource.tags.add(keyword.strip().lower())

            self.stdout.write(self.style.SUCCESS('Successfully loaded all data'))
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f'Error: Could not find file - {str(e)}'))
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f'Error: Invalid JSON in file - {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 