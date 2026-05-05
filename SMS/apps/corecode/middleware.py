from .models import AcademicSession, AcademicTerm
from django.core.exceptions import ObjectDoesNotExist


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        college = getattr(request, 'college', None)
        
        try:
            # Filter by college
            current_session = AcademicSession.objects.filter(current=True, college=college).first()
        except ObjectDoesNotExist:
            current_session = None
            
        try:
            # Filter by college
            current_term = AcademicTerm.objects.filter(current=True, college=college).first()
        except ObjectDoesNotExist:
            current_term = None

        request.current_session = current_session
        request.current_term = current_term

        response = self.get_response(request)

        return response
