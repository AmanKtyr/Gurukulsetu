from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta


class SubscriptionPlan(models.Model):
    """Model for subscription plans"""
    name = models.CharField(_("Plan Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True, null=True)
    duration_months = models.PositiveIntegerField(_("Duration (Months)"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    features = models.TextField(_("Features"), blank=True, null=True)
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.duration_months} months) - ₹{self.price}"

    class Meta:
        ordering = ['price']
        verbose_name = _("Subscription Plan")
        verbose_name_plural = _("Subscription Plans")


class College(models.Model):
    """Model for colleges managed by the super admin"""
    name = models.CharField(_("College Name"), max_length=200)
    code = models.CharField(_("College Code"), max_length=20, unique=True)
    address = models.TextField(_("Address"))
    city = models.CharField(_("City"), max_length=100)
    state = models.CharField(_("State"), max_length=100)
    pincode = models.CharField(_("PIN Code"), max_length=10)
    email = models.EmailField(_("Email"), max_length=100)
    phone = models.CharField(_("Phone"), max_length=20)
    website = models.URLField(_("Website"), blank=True, null=True)
    logo = models.ImageField(_("Logo"), upload_to="college_logos/", blank=True, null=True)
    description = models.TextField(_("Description"), blank=True, null=True)

    # Subscription details
    subscription_start_date = models.DateField(_("Subscription Start Date"), blank=True, null=True)
    subscription_end_date = models.DateField(_("Subscription End Date"), blank=True, null=True)
    subscription_plan = models.CharField(_("Subscription Plan"), max_length=50, blank=True, null=True)
    subscription_plan_ref = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, blank=True, null=True, related_name="colleges", verbose_name=_("Subscription Plan Reference"))

    # Admin credentials
    admin_username = models.CharField(_("Admin Username"), max_length=50, blank=True, null=True)
    admin_email = models.EmailField(_("Admin Email"), max_length=100, blank=True, null=True)

    # Status and timestamps
    is_active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("College")
        verbose_name_plural = _("Colleges")
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("college_detail", kwargs={"pk": self.pk})

    def is_subscription_active(self):
        """Check if the college subscription is active"""
        if not self.subscription_end_date:
            return False
        return self.subscription_end_date >= datetime.now().date()

    def extend_subscription(self, plan, start_date=None):
        """Extend subscription based on the selected plan"""
        if not start_date:
            # If no start date provided, use today or current end date if it's in the future
            today = datetime.now().date()
            if self.subscription_end_date and self.subscription_end_date > today:
                start_date = self.subscription_end_date
            else:
                start_date = today

        # Calculate end date based on plan duration
        end_date = start_date + timedelta(days=30 * plan.duration_months)

        # Update subscription details
        self.subscription_start_date = start_date
        self.subscription_end_date = end_date
        self.subscription_plan = plan.name
        self.subscription_plan_ref = plan

        # Update is_active status based on subscription
        self.is_active = True

        self.save()

        # Log subscription extension
        from django.db import models
        try:
            SubscriptionHistory.objects.create(
                college=self,
                plan_name=plan.name,
                start_date=start_date,
                end_date=end_date,
                amount=plan.price,
                action="extended"
            )
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create subscription history: {e}")

        return True

    def get_subscription_status(self):
        """Get the subscription status"""
        if not self.subscription_end_date:
            return "Not Set"

        today = datetime.now().date()
        if self.subscription_end_date < today:
            return "Expired"

        thirty_days_later = today + timedelta(days=30)
        if self.subscription_end_date <= thirty_days_later:
            return "Expiring Soon"

        return "Active"

    def get_days_remaining(self):
        """Get the number of days remaining in the subscription"""
        if not self.subscription_end_date:
            return 0

        today = datetime.now().date()
        if self.subscription_end_date < today:
            return 0

        delta = self.subscription_end_date - today
        return delta.days

    def get_subscription_progress(self):
        """Get the subscription progress as a percentage"""
        if not self.subscription_start_date or not self.subscription_end_date:
            return 0

        today = datetime.now().date()

        # If subscription has expired, return 100%
        if today > self.subscription_end_date:
            return 100

        # If subscription hasn't started yet, return 0%
        if today < self.subscription_start_date:
            return 0

        # Calculate total duration and elapsed duration
        total_days = (self.subscription_end_date - self.subscription_start_date).days
        if total_days <= 0:
            return 100

        elapsed_days = (today - self.subscription_start_date).days

        # Calculate percentage
        percentage = (elapsed_days / total_days) * 100
        return min(100, max(0, percentage))  # Ensure between 0 and 100


class SubscriptionHistory(models.Model):
    """Model to track subscription history"""
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('extended', 'Extended'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]

    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='subscription_history')
    plan_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _("Subscription History")
        verbose_name_plural = _("Subscription Histories")

    def __str__(self):
        return f"{self.college.name} - {self.plan_name} - {self.action} on {self.created_at.strftime('%Y-%m-%d')}"


class UserProfile(models.Model):
    """Model to link users to colleges"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='users', null=True, blank=True)

    # Additional fields for user profile
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

    # Last login tracking
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.college.name if self.college else 'No College'}"

    def update_last_active(self):
        """Update the last active timestamp"""
        self.last_active = datetime.now()
        self.save(update_fields=['last_active'])

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile for each new user"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    instance.profile.save()
