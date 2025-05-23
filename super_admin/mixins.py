from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

class CollegeRequiredMixin(UserPassesTestMixin):
    """
    Mixin that checks if the user has a college associated.
    If not, redirects to the login page.
    """
    permission_denied_message = "Your account is not associated with any college. Please contact the administrator."
    login_url = 'login'
    
    def test_func(self):
        # Superusers can access everything
        if self.request.user.is_superuser:
            return True
            
        # Check if user has a college
        if not hasattr(self.request, 'college') or not self.request.college:
            logger.warning(f"User {self.request.user.username} attempted to access view without college association")
            return False
            
        # Check if college subscription is active
        if hasattr(self.request.college, 'subscription_end_date'):
            from datetime import datetime
            if self.request.college.subscription_end_date and self.request.college.subscription_end_date < datetime.now().date():
                logger.warning(f"User {self.request.user.username} attempted to access view with expired subscription")
                messages.warning(self.request, "Your college subscription has expired. Some features may be limited.")
                # We still allow access but with a warning
                
        return True
        
    def get_queryset(self):
        """
        Filter queryset to only include objects related to the current college.
        """
        queryset = super().get_queryset()
        
        # If user is superuser, return all objects
        if self.request.user.is_superuser:
            return queryset
            
        # If no college is set in the request, return empty queryset
        if not hasattr(self.request, 'college') or not self.request.college:
            logger.warning(f"User {self.request.user.username} attempted to access data without college association")
            return queryset.none()
            
        # Check if the model has a direct college field
        if hasattr(queryset.model, 'college'):
            return queryset.filter(college=self.request.college)
            
        # Check if the model has a college_id field
        if hasattr(queryset.model, 'college_id'):
            return queryset.filter(college_id=self.request.college.id)
            
        # If we can't determine how to filter, log a warning and return empty queryset
        logger.warning(
            f"Could not determine how to filter {queryset.model.__name__} by college. "
            f"User: {self.request.user.username}, College: {self.request.college.name}"
        )
        return queryset.none()
        
    def form_valid(self, form):
        """
        Associate the form instance with the current college.
        """
        # If user is superuser, don't associate with any college
        if self.request.user.is_superuser:
            return super().form_valid(form)
            
        # Check if request has a college
        if not hasattr(self.request, 'college') or not self.request.college:
            logger.warning(f"User {self.request.user.username} attempted to create/update data without college association")
            messages.error(self.request, "You are not associated with any college. Please contact the administrator.")
            return redirect(self.login_url)
            
        # Check if the model has a college field
        if hasattr(form.instance, 'college'):
            form.instance.college = self.request.college
            
        # Check if the model has a college_id field
        elif hasattr(form.instance, 'college_id'):
            form.instance.college_id = self.request.college.id
            
        return super().form_valid(form)
