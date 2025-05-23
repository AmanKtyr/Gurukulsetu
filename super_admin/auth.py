from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import logging
from .models import UserProfile, College

logger = logging.getLogger(__name__)
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
        # First, try to authenticate by username
        try:
            # Check if username is actually an email
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)

            # Check password
            if user.check_password(password):
                return self.post_authenticate(request, user)
        except User.DoesNotExist:
            pass

        # If that fails, try the standard ModelBackend authentication
        user = super().authenticate(request, username=username, password=password, **kwargs)
        if user is not None:
            return self.post_authenticate(request, user)

        return None

    def post_authenticate(self, request, user):
        """
        Process user after authentication is successful
        """
        # If the user is a superuser, they can access everything
        if user.is_superuser:
            if request:
                request.session['is_super_admin'] = True
            return user

        # Ensure the user has a profile
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # Create a profile if it doesn't exist
            profile = UserProfile.objects.create(user=user)
            logger.info(f"Created new profile for user {user.username}")

        # Check if the user has a profile with a college
        try:
            if profile.college:
                # User has a college, set it in the session
                if request:
                    request.session['college_id'] = profile.college.id
                    request.session['college_name'] = profile.college.name

                    # Check if college subscription is active
                    if profile.college.subscription_end_date:
                        from datetime import datetime
                        if profile.college.subscription_end_date < datetime.now().date():
                            logger.warning(f"User {user.username} logged in with expired subscription for college {profile.college.name}")
                            request.session['subscription_expired'] = True
                        else:
                            request.session['subscription_expired'] = False
                    else:
                        request.session['subscription_expired'] = True

                return user
            else:
                # User doesn't have a college
                logger.warning(f"User {user.username} logged in without college association")
                if request:
                    request.session['no_college'] = True
                return user
        except Exception as e:
            # If there's an error, still return the user but log the error
            logger.error(f"Error checking user college: {e}")
            return user
