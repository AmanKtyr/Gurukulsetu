from django.urls import path
from . import views

app_name = 'super_admin'

urlpatterns = [
    # Authentication
    path('login/', views.SuperAdminLoginView.as_view(), name='login'),

    # Dashboard
    path('', views.SuperAdminDashboardView.as_view(), name='dashboard'),

    # College management
    path('colleges/', views.CollegeListView.as_view(), name='college_list'),
    path('colleges/add/', views.CollegeCreateView.as_view(), name='college_create'),
    path('colleges/<int:pk>/', views.CollegeDetailView.as_view(), name='college_detail'),
    path('colleges/<int:pk>/edit/', views.CollegeUpdateView.as_view(), name='college_update'),
    path('colleges/<int:pk>/delete/', views.CollegeDeleteView.as_view(), name='college_delete'),

    # College activation/deactivation
    path('colleges/<int:pk>/toggle-status/', views.toggle_college_status, name='toggle_college_status'),

    # College admin management
    path('colleges/<int:pk>/create-admin/', views.create_college_admin, name='create_college_admin'),
    path('colleges/<int:pk>/reset-admin-password/', views.reset_college_admin_password, name='reset_college_admin_password'),

    # Reports
    path('reports/colleges/', views.CollegeReportView.as_view(), name='college_report'),
    path('reports/subscriptions/', views.SubscriptionReportView.as_view(), name='subscription_report'),

    # Subscription Plans
    path('subscription-plans/', views.SubscriptionPlanListView.as_view(), name='subscription_plan_list'),
    path('subscription-plans/add/', views.SubscriptionPlanCreateView.as_view(), name='subscription_plan_create'),
    path('subscription-plans/<int:pk>/edit/', views.SubscriptionPlanUpdateView.as_view(), name='subscription_plan_update'),
    path('subscription-plans/<int:pk>/delete/', views.SubscriptionPlanDeleteView.as_view(), name='subscription_plan_delete'),

    # Subscription History
    path('subscription-history/', views.SubscriptionHistoryView.as_view(), name='subscription_history'),

    # College Subscription Management
    path('colleges/<int:pk>/subscription/', views.CollegeSubscriptionView.as_view(), name='college_subscription'),
]
