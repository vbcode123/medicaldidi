from django.db import models

class SubAdmin(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    aadhaar_image = models.ImageField(upload_to='aadhaar/')
    profile_photo = models.ImageField(upload_to='profile/')
    joining_date = models.DateField()
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.name


#   ADD NURSE=====================
from django.db import models

class Nurse(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    full_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    dob = models.DateField()
    profile_image = models.ImageField(upload_to='nurse_profile/', null=True, blank=True)
    aadhaar_image = models.ImageField(upload_to='nurse_aadhaar/', null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    certificate_image = models.ImageField(upload_to='nurse_certificates/', null=True, blank=True)
    experience = models.CharField(max_length=200)
    joining_date = models.DateField()
    password = models.CharField(max_length=200, default='')
    is_approved = models.BooleanField(default=False)

    # NEW FIELDS
    parents_name = models.CharField(max_length=200, null=True, blank=True)
    parents_aadhaar_image = models.ImageField(upload_to='nurse_parents_aadhaar/', null=True, blank=True)
    parents_contact_number = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


#Customer Inquirey=====================================================
from django.db import models


class Inquiry(models.Model):
    NURSE_TYPES = (
        ('Male', 'Male Nurse'),
        ('Female', 'Female Nurse'),
    )

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    nurse_type = models.CharField(choices=NURSE_TYPES, max_length=10)
    remark = models.TextField(null=True, blank=True)   # ← Added Field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name


class Patient(models.Model):
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    profile_image = models.ImageField(upload_to='patient_profile/', null=True, blank=True)
    address = models.TextField()
    pin_code = models.CharField(max_length=10)
    aadhaar_image = models.ImageField(upload_to='patient_aadhaar/')
    agreement_image = models.ImageField(upload_to='patient_agreement/', null=True, blank=True)
    patient_representative_name = models.CharField(max_length=200)
    patient_representative_phone = models.CharField(max_length=20)
    password = models.CharField(max_length=200)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def has_active_assignment(self):
        return self.nurse_assignments.filter(status__in=['Pending', 'Approved']).exists()

    def __str__(self):
        return self.full_name


class NurseAssignment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='nurse_assignments')
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='patient_assignments')
    remark = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assigned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('patient', 'nurse')
    
    def __str__(self):
        return f"{self.patient.full_name} -> {self.nurse.full_name}"


class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    
    assignment = models.ForeignKey(NurseAssignment, on_delete=models.CASCADE, related_name='attendances')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_attendances')
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='nurse_attendances')
    date = models.DateField(auto_now_add=True)
    
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_in_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    check_in_approved_at = models.DateTimeField(null=True, blank=True)
    
    check_out_time = models.DateTimeField(null=True, blank=True)
    check_out_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    check_out_approved_at = models.DateTimeField(null=True, blank=True)
    
    total_duty_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_duty_minutes = models.IntegerField(null=True, blank=True)
    total_duty_display = models.CharField(max_length=50, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('nurse', 'patient', 'date')
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.nurse.full_name} - {self.patient.full_name} - {self.date}"


# ==============================================
# LEAVE MANAGEMENT SYSTEM
# ==============================================

class NurseLeave(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='leaves')
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_remark = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-from_date', '-created_at']
    
    def __str__(self):
        return f"{self.nurse.full_name} - {self.from_date} to {self.to_date}"
    
    @property
    def is_active(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.from_date <= today <= self.to_date and self.status == 'Approved'


class TemporaryAssignment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    
    original_assignment = models.ForeignKey(NurseAssignment, on_delete=models.CASCADE, related_name='temporary_assignments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='temporary_assignments')
    replacement_nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE, related_name='temporary_assignments_as_replacement')
    leave = models.ForeignKey(NurseLeave, on_delete=models.CASCADE, related_name='temporary_assignments')
    start_date = models.DateField()
    end_date = models.DateField()
    remark = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"Temp: {self.replacement_nurse.full_name} for {self.patient.full_name}"
    
    @property
    def is_active(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date and self.status == 'Approved'
