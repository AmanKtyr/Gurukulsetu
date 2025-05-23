from django.db import models
import logging

logger = logging.getLogger(__name__)

class CollegeFilteredManager(models.Manager):
    """
    A manager that filters querysets by the college in the request.
    This ensures that users can only see data related to their college.
    """
    
    def get_queryset(self):
        """Return the base queryset"""
        return super().get_queryset()
        
    def for_college(self, request):
        """
        Filter the queryset to only include objects related to the current college.
        
        Args:
            request: The current request object
            
        Returns:
            Filtered queryset containing only objects related to the current college
        """
        queryset = self.get_queryset()
        
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
            
        # If we can't determine how to filter, log a warning and return empty queryset
        logger.warning(
            f"Could not determine how to filter {queryset.model.__name__} by college. "
            f"User: {request.user.username}, College: {request.college.name}"
        )
        return queryset.none()
