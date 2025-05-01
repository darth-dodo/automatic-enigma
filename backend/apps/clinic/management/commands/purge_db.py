from django.core.management.base import BaseCommand
from apps.clinic.models import Role, Staff, Patient, PhoneNumber, Appointment

class Command(BaseCommand):
    help = 'Delete all clinic data'

    def handle(self, *args, **kwargs):
        Appointment.objects.all().delete()
        Patient.objects.all().delete()
        Staff.objects.all().delete()
        Role.objects.all().delete()
        PhoneNumber.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Database purged!'))
