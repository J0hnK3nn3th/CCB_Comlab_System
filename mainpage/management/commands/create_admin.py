from django.core.management.base import BaseCommand
from mainpage.models import ComputerUser


class Command(BaseCommand):
    help = 'Create an admin user for testing'

    def add_arguments(self, parser):
        parser.add_argument('--student_id', type=str, default='ADMIN001', help='Student ID for admin user')
        parser.add_argument('--first_name', type=str, default='Admin', help='First name')
        parser.add_argument('--last_name', type=str, default='User', help='Last name')
        parser.add_argument('--password', type=str, default='admin123', help='Password')
        parser.add_argument('--email', type=str, default='admin@comlab.com', help='Email')

    def handle(self, *args, **options):
        student_id = options['student_id']
        first_name = options['first_name']
        last_name = options['last_name']
        password = options['password']
        email = options['email']

        # Check if admin user already exists
        if ComputerUser.objects.filter(student_id=student_id).exists():
            self.stdout.write(
                self.style.WARNING(f'Admin user with Student ID "{student_id}" already exists.')
            )
            return

        # Create admin user
        admin_user = ComputerUser.objects.create(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact_number='N/A',
            course='System Administrator',
            address='N/A',
            access_level='admin',
            status='active',
            password=password
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created admin user:\n'
                f'Student ID: {admin_user.student_id}\n'
                f'Name: {admin_user.full_name}\n'
                f'Password: {password}\n'
                f'Access Level: {admin_user.access_level}'
            )
        ) 