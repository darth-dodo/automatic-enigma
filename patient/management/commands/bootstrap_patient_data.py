import datetime
import secrets

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker

from patient.models import Patient, PatientDetail, PhoneNumber
from staff.models import Staff

fake = Faker("en_IN")


class Command(BaseCommand):
    help = "Creating Patient data"

    def add_arguments(self, parser):
        pass

    def __init__(self):
        super(Command, self).__init__()
        self.su = Staff.objects.none()

    @transaction.atomic()
    def handle(self, *args, **options):

        self.su = self._su_user_or_error()

        self._staff_present_or_error()

        self._create_phone_numbers(quantity=100)

        count_of_numbers = PhoneNumber.objects.count()
        distinct_count = PhoneNumber.objects.distinct().count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Phones numbers created successfully! \n"
                f"All: {count_of_numbers}\n"
                f"Distinct: {distinct_count}\n"
            )
        )

        self._create_patients_and_patient_details(quantity=50)
        count_of_patients = Patient.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Patients created successfully! \nAll: {count_of_patients}\n"
            )
        )

        self._demo_multiple_phone_numbers(for_patients=4)
        self.stdout.write(
            self.style.SUCCESS("Multiple phone numbers linked successfully! \n")
        )

    def _create_phone_numbers(self, quantity: int) -> None:
        for i in range(1, quantity + 1):
            self._create_phone_number()

    def _create_phone_number(self):
        new_phone_number = PhoneNumber()
        new_phone_number.phone_number = fake.phone_number()
        new_phone_number.is_primary = secrets.choice([True, False])
        new_phone_number.created_by = self.su
        new_phone_number.updated_by = self.su

        if secrets.choice([True, False]):  # nosec
            new_phone_number.note = fake.paragraph()

        new_phone_number.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Phone number created successfully!: {str(new_phone_number)} \n"
            )
        )

    def _create_patients_and_patient_details(self, quantity: int) -> None:
        for i in range(1, quantity + 1):
            patient, staff = self._create_patient()
            self._create_patient_details(patient=patient, staff=staff)

    def _create_patient(self) -> [Patient, Staff]:
        random_staff = Staff.objects.exclude(code="SUPER").order_by("?").first()
        random_contact = (
            PhoneNumber.objects.filter(is_primary=True).order_by("?").first()
        )

        patient = Patient()
        localities = ["Tilak Nagar", "Chheda Nagar", "Garodia Nagar", "Pant Nagar"]

        patient.created_by = patient.updated_by = random_staff

        fake_profile = fake.profile()

        patient.first_name = fake_profile["name"].split(" ")[0]
        patient.last_name = fake_profile["name"].split(" ")[-1]

        patient.gender = "female" if fake_profile["sex"] == "F" else "male"
        patient.age = secrets.randbelow(100)

        patient.joining_date = datetime.datetime.today().date()
        patient.primary_assessment_sheet = fake.url()

        if secrets.choice([True, False]):
            patient.note = fake.paragraph()

        patient.primary_contact = random_contact

        if secrets.choice([True, False]):
            patient.locality = secrets.choice(localities)

        patient.save()

        self.stdout.write(
            self.style.SUCCESS(f"Patient created successfully!: {str(patient)} \n")
        )

        return patient, random_staff

    def _create_patient_details(self, patient: Patient, staff: Staff) -> None:

        patient_detail = PatientDetail()

        patient_detail.patient = patient
        patient_detail.created_by = patient_detail.updated_by = staff

        if secrets.choice([True, False]):
            patient_detail.is_referral = True
            patient_detail.referred_by = Patient.objects.all().order_by("?").first()

        if secrets.choice([True, False]):
            patient_detail.referral_notes = fake.paragraph()

        if secrets.choice([True, False]):
            patient_detail.medical_history = fake.paragraph()

        patient_detail.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Patient details created successfully!: {str(patient_detail)} \n"
            )
        )

        return

    def _demo_multiple_phone_numbers(self, for_patients: int) -> None:
        return

    @staticmethod
    def _su_user_or_error() -> Staff:
        try:
            su = Staff.objects.get(code="SUPER")
        except Staff.DoesNotExist:
            raise CommandError("Bootstrap Staff Data")

        return su

    @staticmethod
    def _staff_present_or_error() -> bool:
        staff_present = Staff.objects.exclude(code="SUPER").count()

        if not staff_present:
            raise CommandError("Bootstrap Staff Data")

        return staff_present
