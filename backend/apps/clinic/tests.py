from django.test import TestCase
from .models import Patient, PhoneNumber

class PatientTestCase(TestCase):
    def test_create_patient(self):
        p = Patient.objects.create(name="John Doe", primary_phone="1234567890")
        phone = PhoneNumber.objects.create(number="1234567890")
        p.phone_numbers.add(phone)
        self.assertEqual(str(p), "John Doe")
