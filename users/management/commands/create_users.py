from django.core.management.base import BaseCommand
from users.models import Account, Tier


class Command(BaseCommand):
    help = "Create random users"

    def handle(self, *args, **kwargs):
        # Create superuser
        Account.objects.create_superuser("admin@admin.com", "123")

        # Create other users
        for i in range(3):
            Account.objects.create_user(f"test{i+1}@test.com", "123")

        self.stdout.write(self.style.SUCCESS("Users created successfully."))
