from django.core.management.base import BaseCommand
from resources.models import Resource, Category
from django.contrib.auth import get_user_model
from django.utils import timezone
import csv
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Import Medium articles from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Preview changes without saving')
        parser.add_argument('--csv-path', type=str, default='resources/medium.csv', help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        dry_run = options['dry_run']

        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'CSV file not found at: {csv_path}'))
            return

        # Get or create categories
        ai_category, _ = Category.objects.get_or_create(name='Artificial Intelligence')
        ml_category, _ = Category.objects.get_or_create(name='Machine Learning')

        # Get or create a default user for imported resources
        default_user, created = User.objects.get_or_create(
            username='medium_importer',
            defaults={
                'email': 'medium_importer@example.com',
                'is_active': True,
                'is_staff': True
            }
        )
        if created:
            self.stdout.write('Created default user for imported resources')
        else:
            self.stdout.write('Using existing default user for imported resources')

        # Remove existing Medium articles if not in dry-run mode
        if not dry_run:
            existing_count = Resource.objects.filter(url__contains='medium.com').count()
            if existing_count > 0:
                self.stdout.write(f'Found {existing_count} existing Medium articles. Removing them...')
                Resource.objects.filter(url__contains='medium.com').delete()
                self.stdout.write('Removed existing Medium articles.')

        imported_count = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('3.Title', '')
                url = row.get('8.Link', '')
                description = row.get('4.Body', '')
                category_name = row.get('1.Tag', 'Artificial Intelligence')

                if not (title and url):
                    self.stdout.write(self.style.WARNING(f'Skipping row with missing title or URL'))
                    continue

                # Select category based on tag
                category = ai_category if category_name == 'Artificial Intelligence' else ml_category

                if dry_run:
                    self.stdout.write(f'Would import: {title}')
                    self.stdout.write(f'- URL: {url}')
                    self.stdout.write(f'- Category: {category.name}')
                    self.stdout.write('---')
                else:
                    Resource.objects.create(
                        title=title,
                        url=url,
                        description=description,
                        category=category,
                        resource_type='blog',
                        author=default_user,
                        created_at=timezone.now(),
                        is_approved=True
                    )
                    imported_count += 1

        if dry_run:
            self.stdout.write(self.style.SUCCESS('Dry run completed. No changes were made.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {imported_count} Medium articles.')) 