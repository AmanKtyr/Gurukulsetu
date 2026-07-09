from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('front-office/inquiries/', views.AdmissionInquiryListView.as_view(), name='inquiries'),
    path('front-office/visitor-book/', views.VisitorBookListView.as_view(), name='visitor_book'),
    path('front-office/phone-log/', views.PhoneCallLogListView.as_view(), name='phone_call_log'),
    path('front-office/complaints/', views.ComplaintListView.as_view(), name='complaints'),
]
