from django import forms
from django.utils.translation import gettext_lazy as _
from .models import College, SubscriptionPlan
from datetime import datetime


class SubscriptionPlanForm(forms.ModelForm):
    """Form for creating and updating subscription plans"""
    class Meta:
        model = SubscriptionPlan
        fields = ['name', 'description', 'duration_months', 'price', 'features', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'features': forms.Textarea(attrs={'rows': 5}),
        }


class CollegeSubscriptionForm(forms.Form):
    """Form for managing college subscriptions"""
    subscription_plan = forms.ModelChoiceField(
        queryset=SubscriptionPlan.objects.filter(is_active=True),
        label=_("Subscription Plan"),
        required=True,
        empty_label=_("Select a plan"),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    start_date = forms.DateField(
        label=_("Start Date"),
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        self.college = kwargs.pop('college', None)
        super().__init__(*args, **kwargs)
        
        # Set initial start date to today
        self.fields['start_date'].initial = datetime.now().date()
        
        # Add help text based on college's current subscription
        if self.college and self.college.subscription_end_date:
            if self.college.is_subscription_active():
                self.fields['start_date'].help_text = _(
                    f"Current subscription ends on {self.college.subscription_end_date}. "
                    f"Leave blank to start new subscription after current one ends."
                )
            else:
                self.fields['start_date'].help_text = _(
                    f"Previous subscription ended on {self.college.subscription_end_date}. "
                    f"Leave blank to start new subscription from today."
                )
