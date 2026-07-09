from django.db import models

class AdmissionInquiry(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Passive', 'Passive'),
        ('Dead', 'Dead'),
        ('Won', 'Won'),
        ('Lost', 'Lost'),
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    next_follow_up_date = models.DateField(blank=True, null=True)
    assigned_to = models.CharField(max_length=200, blank=True, null=True)
    reference = models.CharField(max_length=200, blank=True, null=True)
    source = models.CharField(max_length=200, blank=True, null=True)
    class_interested = models.CharField(max_length=100, blank=True, null=True)
    number_of_child = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.name} - {self.class_interested}"


class VisitorBook(models.Model):
    purpose = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    id_card = models.CharField(max_length=100, blank=True, null=True)
    number_of_person = models.IntegerField(default=1)
    date = models.DateField(auto_now_add=True)
    in_time = models.TimeField(blank=True, null=True)
    out_time = models.TimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.purpose}"


class PhoneCallLog(models.Model):
    CALL_TYPES = (
        ('Incoming', 'Incoming'),
        ('Outgoing', 'Outgoing'),
    )
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    next_follow_up_date = models.DateField(blank=True, null=True)
    call_duration = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    call_type = models.CharField(max_length=20, choices=CALL_TYPES, default='Incoming')

    def __str__(self):
        return f"{self.name} ({self.call_type})"


class Complaint(models.Model):
    COMPLAINT_TYPES = (
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('Parent', 'Parent'),
        ('Other', 'Other'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    )
    complaint_type = models.CharField(max_length=50, choices=COMPLAINT_TYPES, default='Student')
    source = models.CharField(max_length=200, blank=True, null=True)
    complainant = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    action_taken = models.TextField(blank=True, null=True)
    assigned_to = models.CharField(max_length=200, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.complainant} - {self.status}"
