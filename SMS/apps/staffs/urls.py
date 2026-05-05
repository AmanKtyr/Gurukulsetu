from django.urls import path
from . import views

from .views import (
    StaffCreateView,
    StaffDeleteView,
    StaffDetailView,
    StaffListView,
    StaffUpdateView,
)

urlpatterns = [
    path("list/", StaffListView.as_view(), name="staff-list"),
    path("<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("create/", StaffCreateView.as_view(), name="staff-create"),
    path("<int:pk>/update/", StaffUpdateView.as_view(), name="staff-update"),
    path("<int:pk>/delete/", StaffDeleteView.as_view(), name="staff-delete"),
    path("salary/", views.staff_salary_list, name="staff-salary"),
    path("salary/pay/", views.make_salary_payment, name="salary-pay"),
    path("salary/edit/", views.edit_staff_salary, name="salary-edit"),
]
