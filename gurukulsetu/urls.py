"""
URL configuration for gurukulsetu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('super-admin/', include('super_admin.urls')),
    path('administration/', include('apps.administration.urls')),
    path('students/', include('apps.students.urls')),
    path('teachers/', include('apps.teachers.urls')),
    path('academics/', include('apps.academics.urls')),
    path('finance/', include('apps.finance.urls')),
    path('transport/', include('apps.transport.urls')),
    path('hostel/', include('apps.hostel.urls')),
    path('library/', include('apps.library.urls')),
    path('communication/', include('apps.communication.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
