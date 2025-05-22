from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


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
