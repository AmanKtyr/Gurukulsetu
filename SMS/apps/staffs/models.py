from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
import random
from super_admin.models import College
from super_admin.managers import CollegeFilteredManager

class Staff(models.Model):
    STATUS = [("active", "Active"), ("inactive", "Inactive")]
    GENDER = [("male", "Male"), ("female", "Female")]

    # College field to associate staff with a specific college
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name='staff_members',
        null=True,
        blank=True
    )

    current_status = models.CharField(max_length=10, choices=STATUS, default="active")
    registration_number = models.CharField(max_length=200, unique=True)
    fullname = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    date_of_registration = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    mobile_number = models.CharField(validators=[mobile_num_regex], max_length=13, blank=True)
    aadhar_validator = RegexValidator(
    regex=r'^\d{12}$',
    message="Aadhaar number must be exactly 12 digits.",
    code='invalid_aadhar'
    )
    aadhar = models.CharField(validators=[aadhar_validator], max_length=12, blank=True)
    Subject_specification = models.TextField(blank=True)
    address = models.TextField(blank=True)
    others = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="staffs/passports/")



    def registration_number(self):
      if self.date_of_registration:
        year_suffix = str(self. date_of_registration.year)[-2:]  # Extract last 2 digits of year
      else:
        year_suffix = "25"  # Default if date_of_admission is missing

      unique_number = str(random.randint(1000, 9999))
      return f"{year_suffix}{unique_number}"

    def __str__(self):
        return f"{self.fullname}"

    def get_absolute_url(self):
        return reverse("staff-detail", kwargs={"pk": self.pk})

    # Add custom manager
    objects = models.Manager()  # Default manager
    college_objects = CollegeFilteredManager()

class StaffSalary(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name="salary_info")
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # College field
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name='staff_salaries',
        null=True,
        blank=True
    )

    @property
    def net_salary(self):
        return self.basic_salary + self.allowances - self.deductions

    def __str__(self):
        return f"{self.staff.fullname} - {self.net_salary}"

class SalaryPayment(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
    ]
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="salary_payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=timezone.now)
    month = models.IntegerField() # 1-12
    year = models.IntegerField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='Cash')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    # College field
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
        related_name='salary_payments',
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ['staff', 'month', 'year']

    def __str__(self):
        return f"{self.staff.fullname} - {self.month}/{self.year}"
