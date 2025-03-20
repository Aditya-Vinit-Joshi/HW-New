from django.core.management.base import BaseCommand
from resources.models import Resource, Category
from django.db.models import Q

class Command(BaseCommand):
    help = 'Remove GitHub Projects category and resources'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Preview changes without making them')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # 1. Find GitHub category
        try:
            github_category = Category.objects.get(name="GitHub Projects")
            self.stdout.write(f"Found GitHub Projects category (ID: {github_category.id}) with {github_category.resources.count()} resources")
        except Category.DoesNotExist:
            self.stdout.write(self.style.WARNING("GitHub Projects category not found"))
            github_category = None
            
        # 2. Find all resources with type 'github'
        github_resources = Resource.objects.filter(resource_type="github")
        self.stdout.write(f"Found {github_resources.count()} resources with type 'github'")
        
        # 3. If we have a GitHub category, find all resources in that category
        if github_category:
            category_resources = Resource.objects.filter(category=github_category)
            self.stdout.write(f"Found {category_resources.count()} resources in GitHub Projects category")
            
            # Combine both queries to get all GitHub resources
            all_github_resources = Resource.objects.filter(
                Q(resource_type="github") | Q(category=github_category)
            ).distinct()
            self.stdout.write(f"Total GitHub resources to remove: {all_github_resources.count()}")
        else:
            # Just use the resource type
            all_github_resources = github_resources
            self.stdout.write(f"Total GitHub resources to remove: {all_github_resources.count()}")
        
        # 4. Delete resources and category if not in dry run mode
        if not dry_run:
            # Delete GitHub resources
            deleted_count = all_github_resources.delete()[0]
            self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} GitHub resources"))
            
            # Delete GitHub category if it exists
            if github_category:
                github_category.delete()
                self.stdout.write(self.style.SUCCESS("Deleted GitHub Projects category"))
            
            self.stdout.write(self.style.SUCCESS("Cleanup completed"))
        else:
            self.stdout.write(self.style.SUCCESS("Dry run completed. No changes were made."))
            
        # 5. Show remaining categories
        self.stdout.write("\nRemaining categories:")
        for category in Category.objects.all():
            self.stdout.write(f"- {category.name}: {category.resources.count()} resources") 