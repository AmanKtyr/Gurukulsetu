"""
Script to create UserProfile objects for all users that don't have one.
"""
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_app.settings')
django.setup()

from django.contrib.auth.models import User
from super_admin.models import UserProfile, College

def create_profiles():
    """Create UserProfile objects for all users that don't have one."""
    users_without_profile = []
    
    for user in User.objects.all():
        try:
            # Check if the user has a profile
            profile = user.profile
        except UserProfile.DoesNotExist:
            # Create a profile for the user
            users_without_profile.append(user.username)
            UserProfile.objects.create(user=user)
    
    return users_without_profile

if __name__ == '__main__':
    users = create_profiles()
    if users:
        print(f"Created profiles for {len(users)} users: {', '.join(users)}")
    else:
        print("All users already have profiles.")
