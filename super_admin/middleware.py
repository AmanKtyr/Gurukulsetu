from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
import logging
from .models import UserProfile, College


logger = logging.getLogger(__name__)


class CollegeMiddleware(MiddlewareMixin):
    """Middleware to add college information to the request and enforce access control"""

    def process_request(self, request):
        """
        Add college information to the request if the user is authenticated
        and enforce access control based on college association
        """
        # Public URLs that don't require college association
        public_urls = [
            '/admin/',
            '/login/',
            '/logout/',
            '/super-admin/login/',
            '/super-admin/dashboard/',
            '/',  # Website root
            '/website/',
            '/about/',
            '/contact/',
            '/features/',
            '/pricing/',
            '/static/',
            '/media/',
        ]

        # Check if current URL is public
        current_path = request.path
        is_public = any(current_path.startswith(url) for url in public_urls)

        # Set default college to None
        request.college = None

        if not request.user.is_authenticated:
            # For unauthenticated users, just return
            return None

        # Skip for superusers - they can see all colleges
        if request.user.is_superuser:
            return None

        try:
            # Get the user's profile and associated college
            try:
                profile = UserProfile.objects.get(user=request.user)
                request.college = profile.college
            except UserProfile.DoesNotExist:
                # Create a profile if it doesn't exist
                profile = UserProfile.objects.create(user=request.user)
                request.college = None

            # If user should have a college but doesn't, and trying to access protected area
            if not request.college and not is_public and not current_path.startswith('/super-admin/'):
                logger.warning(f"User {request.user.username} attempted to access {current_path} without college association")
                messages.error(request, "Your account is not associated with any college. Please contact the administrator.")
                return redirect('login')

        except Exception as e:
            logger.error(f"Error in CollegeMiddleware: {str(e)}")
            request.college = None

        return None
