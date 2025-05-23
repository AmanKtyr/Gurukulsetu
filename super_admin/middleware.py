from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from .models import UserProfile, College


class CollegeMiddleware(MiddlewareMixin):
    """Middleware to add college information to the request"""

    def process_request(self, request):
        """Add college information to the request if the user is authenticated"""
        if request.user.is_authenticated:
            # Skip for superusers - they can see all colleges
            if request.user.is_superuser:
                request.college = None
                return None

            try:
                # Get the user's profile and associated college
                try:
                    profile = UserProfile.objects.get(user=request.user)
                except UserProfile.DoesNotExist:
                    # Create a profile if it doesn't exist
                    profile = UserProfile.objects.create(user=request.user)

                request.college = profile.college
            except Exception:
                request.college = None
        else:
            request.college = None

        return None
