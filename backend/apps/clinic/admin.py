from django.contrib import admin
from .models import Role, Staff, Patient, PhoneNumber, Appointment

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'supervisor']
    search_fields = ['user__username']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    search_fields = ['name', 'primary_phone']

@admin.register(PhoneNumber)
class PhoneNumberAdmin(admin.ModelAdmin):
    search_fields = ['number']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'staff', 'status', 'scheduled_time']
    search_fields = ['patient__name', 'staff__user__username']
    list_filter = ['status']
