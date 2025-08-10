from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    help = 'Create demo user with specified credentials'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create demo user
            demo_email = 'xyz@gmail.com'
            demo_password = 'abcdefghijk'
            
            # Check if user already exists
            if User.objects.filter(email=demo_email).exists():
                self.stdout.write(
                    self.style.WARNING(f'Demo user with email {demo_email} already exists')
                )
                return
            
            # Create the demo user
            demo_user = User.objects.create_user(
                username='xeox_demo',
                email=demo_email,
                password=demo_password,
                first_name='Xeox',
                last_name='Demo',
                bio='Welcome to Xeox! This is a demo account to explore all features.',
                is_verified=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created demo user:\n'
                    f'- Email: {demo_email}\n'
                    f'- Password: {demo_password}\n'
                    f'- Username: {demo_user.username}'
                )
            )
