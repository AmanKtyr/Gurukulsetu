from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import UserProfile

User = get_user_model()

class CollegeUserBackend(ModelBackend):
    """
    Custom authentication backend that checks if the user is associated with a college
    and sets the college in the session.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user and set their college in the session if they have one.
        """
        # First, authenticate the user using the standard ModelBackend
        user = super().authenticate(request, username=username, password=password, **kwargs)

        if user is not None:
            # Ensure the user has a profile
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                # Create a profile if it doesn't exist
                profile = UserProfile.objects.create(user=user)

            # If the user is a superuser, they can access everything
            if user.is_superuser:
                return user

            # Check if the user has a profile with a college
            try:
                if profile.college:
                    # User has a college, set it in the session
                    if request:
                        request.session['college_id'] = profile.college.id
                        request.session['college_name'] = profile.college.name
                    return user
                else:
                    # User doesn't have a college, they might not be allowed to log in
                    # depending on your business rules
                    return user
            except Exception as e:
                # If there's an error, still return the user but log the error
                print(f"Error checking user college: {e}")
                return user

        return None
