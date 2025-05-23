from django.db import transaction
import logging
from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

logger = logging.getLogger(__name__)

def associate_with_college(request, instance):
    """
    Associate a model instance with the current college from the request.

    Args:
        request: The current request object
        instance: The model instance to associate with the college

    Returns:
        True if association was successful, False otherwise
    """
    # If user is superuser, don't associate with any college
    if request.user.is_superuser:
        return True

    # Check if request has a college
    if not hasattr(request, 'college') or not request.college:
        logger.warning(f"User {request.user.username} attempted to create/update data without college association")
        messages.error(request, "You are not associated with any college. Please contact the administrator.")
        return False

    # Check if the model has a college field
    if hasattr(instance, 'college'):
        instance.college = request.college
        return True

    # Check if the model has a college_id field
    if hasattr(instance, 'college_id'):
        instance.college_id = request.college.id
        return True

    # If we can't determine how to associate, log a warning
    logger.warning(
        f"Could not determine how to associate {instance.__class__.__name__} with college. "
        f"User: {request.user.username}, College: {request.college.name}"
    )
    return False

def bulk_associate_with_college(request, queryset):
    """
    Associate multiple model instances with the current college from the request.

    Args:
        request: The current request object
        queryset: The queryset of model instances to associate with the college

    Returns:
        Number of instances successfully associated
    """
    # If user is superuser, don't associate with any college
    if request.user.is_superuser:
        return queryset.count()

    # Check if request has a college
    if not hasattr(request, 'college') or not request.college:
        logger.warning(f"User {request.user.username} attempted to bulk associate data without college association")
        messages.error(request, "You are not associated with any college. Please contact the administrator.")
        return 0

    # Check if the model has a college field
    if hasattr(queryset.model, 'college'):
        with transaction.atomic():
            count = queryset.update(college=request.college)
        return count

    # Check if the model has a college_id field
    if hasattr(queryset.model, 'college_id'):
        with transaction.atomic():
            count = queryset.update(college_id=request.college.id)
        return count

    # If we can't determine how to associate, log a warning
    logger.warning(
        f"Could not determine how to bulk associate {queryset.model.__name__} with college. "
        f"User: {request.user.username}, College: {request.college.name}"
    )
    return 0


def college_required(view_func):
    """
    Decorator for views that checks that the user has a college associated,
    redirecting to the login page if necessary.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')

        # Superusers can access everything
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # Check if user has a college
        if not hasattr(request, 'college') or not request.college:
            logger.warning(f"User {request.user.username} attempted to access view without college association")
            messages.error(request, "Your account is not associated with any college. Please contact the administrator.")
            return redirect('login')

        # Check if college subscription is active
        if hasattr(request.college, 'subscription_end_date'):
            from datetime import datetime
            if request.college.subscription_end_date and request.college.subscription_end_date < datetime.now().date():
                logger.warning(f"User {request.user.username} attempted to access view with expired subscription")
                messages.warning(request, "Your college subscription has expired. Some features may be limited.")
                # We still allow access but with a warning

        return view_func(request, *args, **kwargs)
    return _wrapped_view
