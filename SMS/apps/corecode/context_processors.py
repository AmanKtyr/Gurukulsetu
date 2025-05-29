from .models import AcademicSession, AcademicTerm, SiteConfig, CollegeProfile as CollegeProfileModel
from django.core.exceptions import ObjectDoesNotExist


def site_defaults(request):
    """Context processor for site-wide defaults"""
    contexts = {}

    # Get current session and term based on user's college
    if hasattr(request, 'college') and request.college:
        # Filter by college
        try:
            current_session = AcademicSession.objects.filter(current=True, college=request.college).first()
            current_session_name = current_session.name if current_session else None
        except:
            current_session_name = None

        try:
            current_term = AcademicTerm.objects.filter(current=True, college=request.college).first()
            current_term_name = current_term.name if current_term else None
        except:
            current_term_name = None
    else:
        # Fallback to global current session/term
        try:
            current_session = AcademicSession.objects.filter(current=True).first()
            current_session_name = current_session.name if current_session else None
        except:
            current_session_name = None

        try:
            current_term = AcademicTerm.objects.filter(current=True).first()
            current_term_name = current_term.name if current_term else None
        except:
            current_term_name = None

    contexts.update({
        "current_session": current_session_name,
        "current_term": current_term_name,
    })

    # Add site config values
    try:
        vals = SiteConfig.objects.all()
        for val in vals:
            contexts[val.key] = val.value
    except:
        pass

    # Add college information from session
    if hasattr(request, 'session'):
        contexts.update({
            'college_name': request.session.get('college_name'),
            'college_logo': request.session.get('college_logo'),
            'college_email': request.session.get('college_email'),
            'college_phone': request.session.get('college_phone'),
            'subscription_expired': request.session.get('subscription_expired', False),
            'is_super_admin': request.session.get('is_super_admin', False),
        })

    return contexts


def global_college_profile(request):
    try:
        profile = CollegeProfileModel.objects.first()
    except CollegeProfileModel.DoesNotExist:
        profile = None
    return {'profile': profile}