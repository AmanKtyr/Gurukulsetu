from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse, resolve
from django.contrib import messages
import logging
import re
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
            '/favicon.ico',
            '/robots.txt',
        ]

        # Super admin URLs pattern
        super_admin_pattern = re.compile(r'^/super-admin/')

        # Check if current URL is public
        current_path = request.path
        is_public = any(current_path.startswith(url) for url in public_urls)
        is_super_admin = bool(super_admin_pattern.match(current_path))

        # Set default college to None
        request.college = None

        if not request.user.is_authenticated:
            # For unauthenticated users, just return if it's a public URL
            if is_public:
                return None
            # For non-public URLs, redirect to login
            if not current_path.startswith('/login/'):
                return redirect('login')
            return None

        # Skip for superusers - they can see all colleges
        if request.user.is_superuser:
            # Store in session for templates
            request.session['is_super_admin'] = True
            return None

        # Regular users should not access super admin URLs
        if is_super_admin and not request.user.is_superuser:
            logger.warning(f"Non-superuser {request.user.username} attempted to access super admin area: {current_path}")
            messages.error(request, "You do not have permission to access the super admin area.")
            return redirect('dashboard')

        try:
            # Get the user's profile and associated college
            try:
                profile = UserProfile.objects.get(user=request.user)
                request.college = profile.college

                # Store college info in session for templates
                if request.college:
                    request.session['college_id'] = request.college.id
                    request.session['college_name'] = request.college.name
                    request.session['college_logo'] = request.college.logo.url if request.college.logo else None
                    request.session['college_email'] = request.college.email
                    request.session['college_phone'] = request.college.phone

                    # Check if college subscription is active
                    if request.college.subscription_end_date:
                        from datetime import datetime
                        if request.college.subscription_end_date < datetime.now().date():
                            logger.warning(f"User {request.user.username} logged in with expired subscription for college {request.college.name}")
                            request.session['subscription_expired'] = True

                            # Show warning only once per session for expired subscription
                            if not is_public and not request.session.get('subscription_warning_shown'):
                                messages.warning(request, f"Your college subscription expired on {request.college.subscription_end_date}. Some features may be limited.")
                                request.session['subscription_warning_shown'] = True
                        else:
                            request.session['subscription_expired'] = False
                            request.session.pop('subscription_warning_shown', None)
                    else:
                        request.session['subscription_expired'] = True

                    # Update user's last active timestamp
                    try:
                        profile.update_last_active()
                    except:
                        pass

            except UserProfile.DoesNotExist:
                # Create a profile if it doesn't exist
                profile = UserProfile.objects.create(user=request.user)
                request.college = None

            # If user should have a college but doesn't, and trying to access protected area
            if not request.college and not is_public:
                logger.warning(f"User {request.user.username} attempted to access {current_path} without college association")
                messages.error(request, "Your account is not associated with any college. Please contact the administrator.")
                return redirect('login')

        except Exception as e:
            logger.error(f"Error in CollegeMiddleware: {str(e)}")
            request.college = None

        return None

    def process_response(self, request, response):
        """
        Process the response to add college information to templates
        """
        # Add college information to response context if not already present
        if hasattr(request, 'college') and request.college:
            # For Django templates, we already have the context processor
            # This is mainly for debugging and API responses
            if hasattr(response, 'headers'):
                response.headers['X-College-ID'] = str(request.college.id)
                response.headers['X-College-Name'] = request.college.name

        return response