from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    failed_login_attempts = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
