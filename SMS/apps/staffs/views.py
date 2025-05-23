from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Staff


class StaffListView(LoginRequiredMixin, ListView):
    model = Staff

    def get_queryset(self):
        """Filter staff by college if user is not a superuser"""
        queryset = super().get_queryset()

        # Filter by college if user is not a superuser and has a college assigned
        if not self.request.user.is_superuser and hasattr(self.request, 'college') and self.request.college:
            queryset = queryset.filter(college=self.request.college)

        return queryset


class StaffDetailView(LoginRequiredMixin,DetailView):
    model = Staff
    template_name = "staffs/staff_detail.html"

    def get_queryset(self):
        """Ensure users can only view staff from their college"""
        queryset = super().get_queryset()

        # Filter by college if user is not a superuser and has a college assigned
        if not self.request.user.is_superuser and hasattr(self.request, 'college') and self.request.college:
            queryset = queryset.filter(college=self.request.college)

        return queryset


class StaffCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Staff
    fields = "__all__"
    success_message = "New staff successfully added"

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_registration"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["Subject_specification"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})

        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form

    def form_valid(self, form):
        # Set the college based on the logged-in user's college
        if not self.request.user.is_superuser and hasattr(self.request, 'college') and self.request.college:
            form.instance.college = self.request.college

        return super().form_valid(form)


class StaffUpdateView( LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Staff
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_registration"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["Subject_specification"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form

    def get_queryset(self):
        """Ensure users can only update staff from their college"""
        queryset = super().get_queryset()

        # Filter by college if user is not a superuser and has a college assigned
        if not self.request.user.is_superuser and hasattr(self.request, 'college') and self.request.college:
            queryset = queryset.filter(college=self.request.college)

        return queryset


class StaffDeleteView(LoginRequiredMixin, DeleteView):
    model = Staff
    success_url = reverse_lazy("staff-list")

    def get_queryset(self):
        """Ensure users can only delete staff from their college"""
        queryset = super().get_queryset()

        # Filter by college if user is not a superuser and has a college assigned
        if not self.request.user.is_superuser and hasattr(self.request, 'college') and self.request.college:
            queryset = queryset.filter(college=self.request.college)

        return queryset
