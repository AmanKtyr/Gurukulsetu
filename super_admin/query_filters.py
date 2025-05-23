from django.db.models import Q
import logging

logger = logging.getLogger(__name__)

def filter_by_college(queryset, request):
    """
    Filter a queryset to only include objects related to the current college.
    This is used to ensure data isolation between colleges.
    
    Args:
        queryset: The queryset to filter
        request: The current request object
        
    Returns:
        Filtered queryset containing only objects related to the current college
    """
    # If user is superuser, return all objects
    if request.user.is_superuser:
        return queryset
        
    # If no college is set in the request, return empty queryset
    if not hasattr(request, 'college') or not request.college:
        logger.warning(f"User {request.user.username} attempted to access data without college association")
        return queryset.none()
        
    # Check if the model has a direct college field
    if hasattr(queryset.model, 'college'):
        return queryset.filter(college=request.college)
        
    # Check if the model has a college_id field
    if hasattr(queryset.model, 'college_id'):
        return queryset.filter(college_id=request.college.id)
        
    # Check for related fields that might link to a college
    # This is a more complex case and depends on your data model
    related_fields = [
        'student__college',  # For models related to students
        'staff__college',    # For models related to staff
        'user__profile__college',  # For models related to users
    ]
    
    for field in related_fields:
        try:
            # Try to filter by this related field
            filtered = queryset.filter(**{field: request.college})
            if filtered.exists():
                return filtered
        except Exception:
            # Field doesn't exist on this model, try the next one
            continue
            
    # If we can't determine how to filter, log a warning and return empty queryset
    logger.warning(
        f"Could not determine how to filter {queryset.model.__name__} by college. "
        f"User: {request.user.username}, College: {request.college.name}"
    )
    return queryset.none()
