"""newapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin

# URLs that don't need to be translated
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Language switcher URL
    path('admin/', admin.site.urls),  # Django admin
]

# URLs that should be translated
urlpatterns += i18n_patterns(
    # Landing page from website app
    path("", include("website.urls")),

    # Authentication URLs
    path("accounts/", include("django.contrib.auth.urls")),

    # Dashboard and core functionality
    path("dashboard/", include("apps.corecode.urls")),

    # Other app URLs
    path("student/", include("apps.students.urls")),
    path('attendance/', include(('apps.attendance.urls', 'attendance'))),
    path("staff/", include("apps.staffs.urls")),
    # Finance app removed
    # Result app removed
    path("non-teaching-staffs/", include("apps.NonTeachingStaffs.urls")),
    # Added namespace
    path('fees/', include('apps.fees.urls', namespace='fees')),
    # Exams app
    path('exams/', include('apps.exams.urls', namespace='exams')),
    # Documents app
    path('documents/', include('apps.documents.urls', namespace='documents')),
    # Super Admin app
    path('super-admin/', include('super_admin.urls', namespace='super_admin')),

    prefix_default_language=False,  # Don't add language prefix for default language
)

# Add static/media files handling
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
