from .models import AcademicSession, AcademicTerm
from django.core.exceptions import ObjectDoesNotExist


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            current_session = AcademicSession.objects.get(current=True)
        except ObjectDoesNotExist:
            current_session = None
        try:
            current_term = AcademicTerm.objects.get(current=True)
        except ObjectDoesNotExist:
            current_term = None

        request.current_session = current_session
        request.current_term = current_term

        response = self.get_response(request)

        return response
