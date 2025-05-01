from django.core.management.base import BaseCommand
from apps.clinic.models import Role, Staff, Patient, PhoneNumber
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate DB with sample data'

    def handle(self, *args, **kwargs):
        role, _ = Role.objects.get_or_create(name='Physio')
        user, _ = User.objects.get_or_create(username='staff1', defaults={'email': 'staff1@example.com'})
        user.set_password('password123')
        user.save()
        staff, _ = Staff.objects.get_or_create(user=user, role=role)
        patient, _ = Patient.objects.get_or_create(name='John Doe', primary_phone='1234567890')
        phone, _ = PhoneNumber.objects.get_or_create(number='1234567890')
        patient.phone_numbers.add(phone)
        self.stdout.write(self.style.SUCCESS('Database populated!'))
