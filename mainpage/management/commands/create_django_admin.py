from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a Django admin user for testing auth_user authentication'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Username for admin user')
        parser.add_argument('--password', type=str, default='admin123', help='Password')
        parser.add_argument('--email', type=str, default='admin@comlab.com', help='Email')
        parser.add_argument('--first_name', type=str, default='Admin', help='First name')
        parser.add_argument('--last_name', type=str, default='User', help='Last name')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        first_name = options['first_name']
        last_name = options['last_name']

        # Check if admin user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Django admin user "{username}" already exists.')
            )
            return

        # Create Django admin user
        admin_user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,  # Required for admin access
            is_superuser=True,  # Optional: full admin privileges
            is_active=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created Django admin user:\n'
                f'Username: {admin_user.username}\n'
                f'Name: {admin_user.get_full_name()}\n'
                f'Email: {admin_user.email}\n'
                f'Password: {password}\n'
                f'Staff: {admin_user.is_staff}\n'
                f'Active: {admin_user.is_active}'
            )
        ) 