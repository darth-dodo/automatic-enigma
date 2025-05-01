from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone_number', 'failed_login_attempts']
    search_fields = ['username', 'email', 'phone_number']
    list_filter = ['is_active', 'is_staff', 'is_superuser']
