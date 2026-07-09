from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AdmissionInquiry, VisitorBook, PhoneCallLog, Complaint

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'administration/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Administration Dashboard'
        return context

class AdmissionInquiryListView(LoginRequiredMixin, ListView):
    model = AdmissionInquiry
    template_name = 'administration/admission_inquiries.html'
    context_object_name = 'inquiries'

class VisitorBookListView(LoginRequiredMixin, ListView):
    model = VisitorBook
    template_name = 'administration/visitor_book.html'
    context_object_name = 'visitors'
    ordering = ['-date', '-in_time']

class PhoneCallLogListView(LoginRequiredMixin, ListView):
    model = PhoneCallLog
    template_name = 'administration/phone_call_log.html'
    context_object_name = 'calls'
    ordering = ['-date']

class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = 'administration/complaints.html'
    context_object_name = 'complaints'
    ordering = ['-date']


