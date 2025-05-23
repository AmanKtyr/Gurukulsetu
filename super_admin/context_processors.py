from .models import College, UserProfile

def college_context(request):
    """
    Add college information to the context for all templates.
    This ensures that templates can access the current college information.
    """
    context = {
        'current_college': None,
        'is_super_admin': False,
        'subscription_expired': False,
    }
    
    # Check if user is authenticated
    if hasattr(request, 'user') and request.user.is_authenticated:
        # Check if user is superuser
        if request.user.is_superuser:
            context['is_super_admin'] = True
            
        # Get college from request (set by middleware)
        if hasattr(request, 'college') and request.college:
            context['current_college'] = request.college
            
            # Check if subscription is expired
            if hasattr(request.college, 'subscription_end_date'):
                from datetime import datetime
                if request.college.subscription_end_date and request.college.subscription_end_date < datetime.now().date():
                    context['subscription_expired'] = True
    
    # Get subscription status from session
    if hasattr(request, 'session'):
        if request.session.get('subscription_expired', False):
            context['subscription_expired'] = True
            
    return context
