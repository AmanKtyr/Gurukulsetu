from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
import random
import string

from .models import College, UserProfile, SubscriptionPlan, SubscriptionHistory
from .forms import SubscriptionPlanForm, CollegeSubscriptionForm


# Super Admin Login View
class SuperAdminLoginView(LoginView):
    template_name = 'super_admin/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            # Ensure the user has a profile
            try:
                UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                # Create a profile if it doesn't exist
                UserProfile.objects.create(user=user)

            login(self.request, user)
            messages.success(self.request, _('Welcome to Super Admin Dashboard!'))
            return redirect('super_admin:dashboard')
        else:
            messages.error(self.request, _('Access denied. Only superusers can access this area.'))
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('super_admin:dashboard')


# Mixin to check if user is a superuser
class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


# Dashboard view
class SuperAdminDashboardView(LoginRequiredMixin, SuperUserRequiredMixin, TemplateView):
    template_name = 'super_admin/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get counts for dashboard
        context['total_colleges'] = College.objects.count()
        context['active_colleges'] = College.objects.filter(is_active=True).count()
        context['inactive_colleges'] = College.objects.filter(is_active=False).count()

        # Get colleges with expiring subscriptions (within next 30 days)
        today = datetime.now().date()
        thirty_days_later = today + timedelta(days=30)
        context['expiring_subscriptions'] = College.objects.filter(
            subscription_end_date__range=[today, thirty_days_later],
            is_active=True
        ).order_by('subscription_end_date')

        # Get recently added colleges
        context['recent_colleges'] = College.objects.order_by('-created_at')[:5]

        return context


# College List View
class CollegeListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = College
    template_name = 'super_admin/college_list.html'
    context_object_name = 'colleges'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by search query if provided
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(code__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query)
            )

        # Filter by status if provided
        status_filter = self.request.GET.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(is_active=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(is_active=False)

        return queryset


# College Detail View
class CollegeDetailView(LoginRequiredMixin, SuperUserRequiredMixin, DetailView):
    model = College
    template_name = 'super_admin/college_detail.html'
    context_object_name = 'college'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add today and thirty_days_later for subscription status display
        today = datetime.now().date()
        thirty_days_later = today + timedelta(days=30)
        context['today'] = today
        context['thirty_days_later'] = thirty_days_later

        return context


# College Create View
class CollegeCreateView(LoginRequiredMixin, SuperUserRequiredMixin, CreateView):
    model = College
    template_name = 'super_admin/college_form.html'
    fields = ['name', 'code', 'address', 'city', 'state', 'pincode', 'email',
              'phone', 'website', 'logo', 'description', 'subscription_start_date',
              'subscription_end_date', 'subscription_plan']
    success_url = reverse_lazy('super_admin:college_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('College created successfully.'))

        # Redirect to create admin page for the newly created college
        return redirect('super_admin:create_college_admin', pk=self.object.pk)


# College Update View
class CollegeUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    model = College
    template_name = 'super_admin/college_form.html'
    fields = ['name', 'code', 'address', 'city', 'state', 'pincode', 'email',
              'phone', 'website', 'logo', 'description', 'subscription_start_date',
              'subscription_end_date', 'subscription_plan', 'is_active']
    success_url = reverse_lazy('super_admin:college_list')

    def form_valid(self, form):
        messages.success(self.request, _('College updated successfully.'))
        return super().form_valid(form)


# College Delete View
class CollegeDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = College
    template_name = 'super_admin/college_confirm_delete.html'
    success_url = reverse_lazy('super_admin:college_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('College deleted successfully.'))
        return super().delete(request, *args, **kwargs)


# Toggle college status (activate/deactivate)
@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_college_status(request, pk):
    college = get_object_or_404(College, pk=pk)
    college.is_active = not college.is_active
    college.save()

    status = 'activated' if college.is_active else 'deactivated'
    messages.success(request, _(f'College {status} successfully.'))

    # If AJAX request, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'is_active': college.is_active,
            'message': f'College {status} successfully.'
        })

    return redirect('super_admin:college_list')


# Create college admin user
@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_college_admin(request, pk):
    college = get_object_or_404(College, pk=pk)

    # Generate default username and password if it's a new college without admin
    suggested_username = college.code.lower() if college.code else ''.join(college.name.lower().split())
    suggested_username = ''.join(e for e in suggested_username if e.isalnum())

    # Generate a random password
    def generate_password(length=10):
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(length))

    suggested_password = generate_password()

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, _('Username already exists.'))
            return render(request, 'super_admin/create_college_admin.html', {
                'college': college,
                'suggested_username': suggested_username,
                'suggested_password': suggested_password
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,  # Give staff status to access admin panel
            is_active=True  # Make sure the account is active
        )

        # Update college with admin details
        college.admin_username = username
        college.admin_email = email
        college.save()

        # Associate user with college
        from super_admin.models import UserProfile
        try:
            # Try to get the user's profile
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            # Create a profile if it doesn't exist
            profile = UserProfile.objects.create(user=user)

        # Set the college and save
        profile.college = college
        profile.save()

        messages.success(request, _('College admin created successfully.'))
        return redirect('super_admin:college_detail', pk=college.pk)

    return render(request, 'super_admin/create_college_admin.html', {
        'college': college,
        'suggested_username': suggested_username,
        'suggested_password': suggested_password
    })


# Reset college admin password
@login_required
@user_passes_test(lambda u: u.is_superuser)
def reset_college_admin_password(request, pk):
    college = get_object_or_404(College, pk=pk)

    if not college.admin_username:
        messages.error(request, _('No admin user associated with this college.'))
        return redirect('super_admin:college_detail', pk=college.pk)

    try:
        user = User.objects.get(username=college.admin_username)
    except User.DoesNotExist:
        messages.error(request, _('Admin user not found.'))
        return redirect('super_admin:college_detail', pk=college.pk)

    # Generate a random password
    def generate_password(length=10):
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(length))

    suggested_password = generate_password()

    if request.method == 'POST':
        password = request.POST.get('password')
        user.set_password(password)
        user.save()

        messages.success(request, _('Admin password reset successfully.'))
        return redirect('super_admin:college_detail', pk=college.pk)

    return render(request, 'super_admin/reset_admin_password.html', {
        'college': college,
        'suggested_password': suggested_password
    })


# College Report View
class CollegeReportView(LoginRequiredMixin, SuperUserRequiredMixin, TemplateView):
    template_name = 'super_admin/college_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all colleges
        context['colleges'] = College.objects.all()

        # Get colleges by state
        colleges_by_state = College.objects.values('state').annotate(count=Count('id')).order_by('-count')
        context['colleges_by_state'] = colleges_by_state

        # Get active vs inactive colleges
        context['active_colleges'] = College.objects.filter(is_active=True).count()
        context['inactive_colleges'] = College.objects.filter(is_active=False).count()

        return context


# Subscription Plan List View
class SubscriptionPlanListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = SubscriptionPlan
    template_name = 'super_admin/subscription_plan_list.html'
    context_object_name = 'plans'
    ordering = ['price']


# Subscription Plan Create View
class SubscriptionPlanCreateView(LoginRequiredMixin, SuperUserRequiredMixin, CreateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = 'super_admin/subscription_plan_form.html'
    success_url = reverse_lazy('super_admin:subscription_plan_list')

    def form_valid(self, form):
        messages.success(self.request, _('Subscription plan created successfully.'))
        return super().form_valid(form)


# Subscription Plan Update View
class SubscriptionPlanUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    model = SubscriptionPlan
    form_class = SubscriptionPlanForm
    template_name = 'super_admin/subscription_plan_form.html'
    success_url = reverse_lazy('super_admin:subscription_plan_list')

    def form_valid(self, form):
        messages.success(self.request, _('Subscription plan updated successfully.'))
        return super().form_valid(form)


# Subscription Plan Delete View
class SubscriptionPlanDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = SubscriptionPlan
    template_name = 'super_admin/subscription_plan_confirm_delete.html'
    success_url = reverse_lazy('super_admin:subscription_plan_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Subscription plan deleted successfully.'))
        return super().delete(request, *args, **kwargs)


# College Subscription Management View
class CollegeSubscriptionView(LoginRequiredMixin, SuperUserRequiredMixin, FormView):
    template_name = 'super_admin/college_subscription.html'
    form_class = CollegeSubscriptionForm

    def get_success_url(self):
        return reverse_lazy('super_admin:college_detail', kwargs={'pk': self.kwargs['pk']})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.college = get_object_or_404(College, pk=self.kwargs['pk'])
        kwargs['college'] = self.college
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['college'] = self.college
        return context

    def form_valid(self, form):
        college = get_object_or_404(College, pk=self.kwargs['pk'])
        plan = form.cleaned_data['subscription_plan']
        start_date = form.cleaned_data['start_date']

        # Extend subscription
        college.extend_subscription(plan, start_date)

        messages.success(self.request, _(f'Subscription updated successfully. New end date: {college.subscription_end_date}'))
        return super().form_valid(form)


# Subscription History View
class SubscriptionHistoryView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = SubscriptionHistory
    template_name = 'super_admin/subscription_history.html'
    context_object_name = 'histories'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by college if specified
        college_id = self.request.GET.get('college')
        if college_id:
            queryset = queryset.filter(college_id=college_id)

        # Filter by action if specified
        action = self.request.GET.get('action')
        if action:
            queryset = queryset.filter(action=action)

        # Filter by date range if specified
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(created_at__date__range=[start_date, end_date])
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colleges'] = College.objects.all()
        context['actions'] = dict(SubscriptionHistory.ACTION_CHOICES)

        # Add filter values to context
        context['selected_college'] = self.request.GET.get('college', '')
        context['selected_action'] = self.request.GET.get('action', '')
        context['selected_start_date'] = self.request.GET.get('start_date', '')
        context['selected_end_date'] = self.request.GET.get('end_date', '')

        return context


# Subscription Report View
class SubscriptionReportView(LoginRequiredMixin, SuperUserRequiredMixin, TemplateView):
    template_name = 'super_admin/subscription_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all colleges with subscription details
        context['colleges'] = College.objects.all().order_by('subscription_end_date')

        # Get colleges by subscription plan
        colleges_by_plan = College.objects.values('subscription_plan').annotate(count=Count('id')).order_by('-count')
        context['colleges_by_plan'] = colleges_by_plan

        # Get colleges with expired subscriptions
        today = datetime.now().date()
        context['expired_subscriptions'] = College.objects.filter(subscription_end_date__lt=today).count()

        # Get colleges with subscriptions expiring in the next 30 days
        thirty_days_later = today + timedelta(days=30)
        context['expiring_soon'] = College.objects.filter(
            subscription_end_date__range=[today, thirty_days_later]
        ).count()

        # Get colleges with no subscription end date
        context['no_subscription_end_date'] = College.objects.filter(subscription_end_date__isnull=True).count()

        # Add today and thirty_days_later to context for template use
        context['today'] = today
        context['thirty_days_later'] = thirty_days_later

        # Get all subscription plans
        context['subscription_plans'] = SubscriptionPlan.objects.filter(is_active=True)

        # Get recent subscription activities
        context['recent_activities'] = SubscriptionHistory.objects.all().order_by('-created_at')[:10]

        # Calculate total revenue
        total_revenue = SubscriptionHistory.objects.filter(
            action__in=['created', 'extended'],
            created_at__gte=today - timedelta(days=365)  # Last year
        ).aggregate(total=Sum('amount'))['total'] or 0
        context['total_revenue'] = total_revenue

        # Calculate monthly revenue for the last 6 months
        monthly_revenue = []
        for i in range(5, -1, -1):
            month_start = (today.replace(day=1) - timedelta(days=i*30)).replace(day=1)
            if i > 0:
                month_end = (today.replace(day=1) - timedelta(days=(i-1)*30)).replace(day=1) - timedelta(days=1)
            else:
                month_end = today

            amount = SubscriptionHistory.objects.filter(
                action__in=['created', 'extended'],
                created_at__date__range=[month_start, month_end]
            ).aggregate(total=Sum('amount'))['total'] or 0

            monthly_revenue.append({
                'month': month_start.strftime('%b %Y'),
                'amount': amount
            })

        context['monthly_revenue'] = monthly_revenue

        return context
