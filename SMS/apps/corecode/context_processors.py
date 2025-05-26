from .models import AcademicSession, AcademicTerm, SiteConfig, CollegeProfile as CollegeProfileModel
from django.core.exceptions import ObjectDoesNotExist


def site_defaults(request):
    try:
        current_session = AcademicSession.objects.get(current=True)
        current_session_name = current_session.name
    except ObjectDoesNotExist:
        current_session_name = None
    try:
        current_term = AcademicTerm.objects.get(current=True)
        current_term_name = current_term.name
    except ObjectDoesNotExist:
        current_term_name = None
    vals = SiteConfig.objects.all()
    contexts = {
        "current_session": current_session_name,
        "current_term": current_term_name,
    }
    for val in vals:
        contexts[val.key] = val.value

    return contexts


def global_college_profile(request):  
    try:
        profile = CollegeProfileModel.objects.first()  
    except CollegeProfileModel.DoesNotExist:
        profile = None
    return {'profile': profile}