from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import widgets
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import transaction

from .models import Staff, StaffSalary, SalaryPayment


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

@login_required
def staff_salary_list(request):
    """View to list staff and their salary status"""
    staff_query = Staff.objects.filter(current_status='active')
    
    # Filter by college
    if not request.user.is_superuser and hasattr(request, 'college') and request.college:
        staff_query = staff_query.filter(college=request.college)
        
    staff_list = staff_query.order_by('fullname')
    
    # Get current month and year
    from django.utils import timezone
    now = timezone.now()
    current_month = now.month
    current_year = now.year
    
    # Get all salary payments for this month/year
    payments = SalaryPayment.objects.filter(month=current_month, year=current_year)
    payment_dict = {p.staff_id: p for p in payments}
    
    # Attach salary info and payment status to each staff
    for staff in staff_list:
        salary_info, created = StaffSalary.objects.get_or_create(
            staff=staff,
            defaults={'college': getattr(request, 'college', None)}
        )
        staff.salary_info = salary_info
        staff.is_paid = staff.id in payment_dict
        if staff.is_paid:
            staff.payment_info = payment_dict[staff.id]

    context = {
        'staff_list': staff_list,
        'current_month': current_month,
        'current_year': current_year,
    }
    return render(request, 'staffs/staff_salary_list.html', context)

@login_required
def make_salary_payment(request):
    """AJAX view to process salary payment"""
    if request.method != 'POST':
        return JsonResponse({'message': 'Method not allowed'}, status=405)
        
    staff_id = request.POST.get('staff_id')
    amount = request.POST.get('amount')
    month = request.POST.get('month')
    year = request.POST.get('year')
    
    staff = get_object_or_404(Staff, id=staff_id)
    college = getattr(request, 'college', None)
    
    try:
        payment, created = SalaryPayment.objects.update_or_create(
            staff=staff,
            month=month,
            year=year,
            defaults={
                'amount_paid': amount,
                'college': college,
                'payment_method': request.POST.get('payment_method', 'Cash'),
                'note': request.POST.get('note', '')
            }
        )
        return JsonResponse({'message': f'Salary paid to {staff.fullname} successfully!'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@login_required
def edit_staff_salary(request):
    """AJAX view to update staff salary settings"""
    if request.method != 'POST':
        return JsonResponse({'message': 'Method not allowed'}, status=405)
        
    staff_id = request.POST.get('staff_id')
    staff = get_object_or_404(Staff, id=staff_id)
    
    try:
        salary_info, created = StaffSalary.objects.get_or_create(
            staff=staff,
            defaults={'college': getattr(request, 'college', None)}
        )
        
        salary_info.basic_salary = request.POST.get('basic_salary', 0)
        salary_info.allowances = request.POST.get('allowances', 0)
        salary_info.deductions = request.POST.get('deductions', 0)
        salary_info.save()
        
        return JsonResponse({'message': f'Salary settings for {staff.fullname} updated successfully!'})
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)
