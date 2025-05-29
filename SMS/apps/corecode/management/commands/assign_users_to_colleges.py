from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from super_admin.models import College, UserProfile


class Command(BaseCommand):
    help = 'Assign existing users to colleges'

    def add_arguments(self, parser):
        parser.add_argument(
            '--college-id',
            type=int,
            help='College ID to assign users to (if not provided, will use first college)',
        )
        parser.add_argument(
            '--create-profiles',
            action='store_true',
            help='Create user profiles for users who don\'t have them',
        )

    def handle(self, *args, **options):
        college_id = options.get('college_id')
        create_profiles = options.get('create_profiles', False)

        # Get the college
        if college_id:
            try:
                college = College.objects.get(id=college_id)
            except College.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'College with ID {college_id} does not exist')
                )
                return
        else:
            college = College.objects.first()
            if not college:
                self.stdout.write(
                    self.style.ERROR('No colleges found. Please create a college first.')
                )
                return

        self.stdout.write(f'Using college: {college.name}')

        # Get all users
        users = User.objects.all()
        assigned_count = 0
        created_profiles = 0

        for user in users:
            # Skip superusers
            if user.is_superuser:
                self.stdout.write(f'Skipping superuser: {user.username}')
                continue

            # Get or create user profile
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                if create_profiles:
                    profile = UserProfile.objects.create(user=user)
                    created_profiles += 1
                    self.stdout.write(f'Created profile for user: {user.username}')
                else:
                    self.stdout.write(f'No profile found for user: {user.username}')
                    continue

            # Assign college if not already assigned
            if not profile.college:
                profile.college = college
                profile.save()
                assigned_count += 1
                self.stdout.write(f'Assigned {user.username} to {college.name}')
            else:
                self.stdout.write(f'User {user.username} already assigned to {profile.college.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully assigned {assigned_count} users to {college.name}'
            )
        )
        
        if created_profiles > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {created_profiles} user profiles'
                )
            )
