from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Fix profile picture issues by clearing invalid profile picture references'

    def handle(self, *args, **options):
        users_fixed = 0
        
        for user in User.objects.all():
            if user.profile_picture:
                # Check if the file actually exists
                try:
                    if not user.profile_picture.file:
                        # File doesn't exist, clear the field
                        user.profile_picture = None
                        user.save()
                        users_fixed += 1
                        self.stdout.write(f'Fixed profile picture for user: {user.username}')
                except (ValueError, FileNotFoundError):
                    # File doesn't exist or is invalid, clear the field
                    user.profile_picture = None
                    user.save()
                    users_fixed += 1
                    self.stdout.write(f'Fixed profile picture for user: {user.username}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {users_fixed} profile pictures')
        )
