from django.db import models
from django.conf import settings

class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_staff')

    def __str__(self):
        return f"{self.user.username} ({self.role.name if self.role else 'No Role'})"

class PhoneNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.number

class Patient(models.Model):
    name = models.CharField(max_length=100)
    primary_phone = models.CharField(max_length=20)
    credit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone_numbers = models.ManyToManyField(PhoneNumber, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='appointments')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('done', 'Done'), ('cancelled', 'Cancelled')])
    scheduled_time = models.DateTimeField()
    notes = models.TextField(blank=True)
    followups = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='followed_by')

    def __str__(self):
        return f"{self.patient.name} with {self.staff.user.username} at {self.scheduled_time}"
