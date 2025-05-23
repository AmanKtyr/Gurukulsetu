from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from super_admin.models import UserProfile


class Command(BaseCommand):
    help = 'Create UserProfile objects for all users that do not have one'

    def handle(self, *args, **options):
        users_without_profile = []
        profiles_created = 0
        
        for user in User.objects.all():
            try:
                # Check if the user has a profile
                user.profile
            except UserProfile.DoesNotExist:
                # Create a profile for the user
                users_without_profile.append(user.username)
                UserProfile.objects.create(user=user)
                profiles_created += 1
        
        if profiles_created > 0:
            self.stdout.write(self.style.SUCCESS(
                f'Created {profiles_created} profiles for users: {", ".join(users_without_profile)}'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('All users already have profiles.'))
