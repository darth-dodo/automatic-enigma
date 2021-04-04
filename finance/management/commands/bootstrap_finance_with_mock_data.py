import datetime
import secrets

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Count
from faker import Faker

from appointment.models import Appointment
from finance.constants import (
    APPOINTMENT_PRESENT_STATE_TITLE,
    INTERNAL_CREDIT_MODE,
    PER_SESSIONS_RATE,
)
from finance.models import Credit, Payment, PaymentMode
from patient.models import Patient
from staff.models import Staff

fake = Faker("en_IN")

"""

appointments_grouped_by_patients = Appointment.objects.values('patient').annotate(count=Count('id')).order_by('-count')[:10]


"""


class Command(BaseCommand):
    help = "Bootstrapping Finance App with Mock data"

    def add_arguments(self, parser):
        pass

    @transaction.atomic()
    def handle(self, *args, **options):

        self._raise_error_if_staff_data_not_bootstrapped()
        self._raise_error_if_patient_data_not_bootstrapped()
        self._raise_error_if_appointment_data_not_bootstrapped()

        self._create_payment_modes()

        self._create_credit_and_payments_for_patients(number=5)

        self._create_ad_hoc_payments()

        self.stdout.write(self.style.SUCCESS("Finance Data successfully bootstrapped"))

    @staticmethod
    def _raise_error_if_staff_data_not_bootstrapped():
        staff_data_exists = Staff.objects.active().exists()
        if not staff_data_exists:
            raise CommandError("Please bootstrap Staff Data")

    @staticmethod
    def _raise_error_if_patient_data_not_bootstrapped():
        patient_data_exists = Patient.objects.exists()
        if not patient_data_exists:
            raise CommandError("Please bootstrap Patient Data")

    @staticmethod
    def _raise_error_if_appointment_data_not_bootstrapped():
        appointment_data_exists = Appointment.objects.exists()
        if not appointment_data_exists:
            raise CommandError("Please bootstrap Appointment Data")

    def _create_payment_modes(self) -> None:
        modes = ["Cash", "G Pay", "Credit Card", INTERNAL_CREDIT_MODE, "Goodwill"]
        su = Staff.objects.get(id__username="SuperUser")

        for mode in modes:
            new_mode = PaymentMode()
            new_mode.created_by = new_mode.updated_by = su
            new_mode.title = mode
            new_mode.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"New Payment Mode successfully bootstrapped: {new_mode}"
                )
            )

        self.stdout.write(self.style.SUCCESS("\n"))

    def _create_credit_and_payments_for_patients(self, number: int = 10):
        """
        group appointments by patients
        make bulk credit deposit when first appointment
        attach new payments for each appointment linked to the credit
        """

        appointments_grouped_by_patients = (
            Appointment.objects.values("patient")
            .annotate(count=Count("id"))
            .order_by("-count")[:number]
        )

        for patient_data in appointments_grouped_by_patients:
            patient = Patient.objects.get(id=patient_data["patient"])
            no_of_sessions = patient_data["count"]
            self._set_credit(for_sessions=no_of_sessions, patient=patient)
            patient.refresh_from_db()
            self._make_payments_for_patient_from_credit(patient=patient)

    def _set_credit(self, for_sessions: int, patient: Patient):

        su = Staff.objects.get(id__username="SuperUser")

        per_session_rate = PER_SESSIONS_RATE
        total_credit = per_session_rate * for_sessions
        one_year_from_now = datetime.datetime.today() + datetime.timedelta(weeks=52)
        payment_mode = self._random_payment_mode()

        credit = Credit()
        credit.created_by = credit.updated_by = su
        credit.patient = patient
        credit.total_amount = credit.balance = total_credit
        credit.valid_until = one_year_from_now.date()
        credit.payment_mode = payment_mode
        credit.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"New Credit successfully bootstrapped: {credit} across patient {credit.patient}"
            )
        )

        self.stdout.write(self.style.SUCCESS("\n"))

    @staticmethod
    def _random_payment_mode() -> PaymentMode:
        return (
            PaymentMode.objects.exclude(title=INTERNAL_CREDIT_MODE)
            .order_by("?")
            .first()
        )

    def _make_payments_for_patient_from_credit(self, patient: Patient):
        patient.refresh_from_db()
        credit = patient.credits.first()

        # mark only present appointments as paid
        appointments = patient.appointments.filter(
            state__title=APPOINTMENT_PRESENT_STATE_TITLE
        )

        for appointment in appointments:

            credit.refresh_from_db()
            print(
                f"Credit before creating payment: {credit.total_amount} | {credit.balance}"
            )
            self._create_payment(appointment=appointment, credit=credit)

            credit.refresh_from_db()
            print(
                f"Credit after creating payment: {credit.total_amount} | {credit.balance}"
            )

    def _create_payment(
        self,
        appointment: Appointment,
        credit: [None, Credit] = None,
        amount: int = PER_SESSIONS_RATE,
    ):

        internal_credit_payment_mode = PaymentMode.objects.get(
            title=INTERNAL_CREDIT_MODE
        )

        new_payment = Payment()
        new_payment.created_by = new_payment.updated_by = appointment.staff
        new_payment.appointment = appointment

        new_payment.amount = amount

        # timeslot, patient, staff are set automatically in the payment model clean() since copied from the appointment

        if credit:
            new_payment.mode = internal_credit_payment_mode
            new_payment.credit = credit
        else:
            new_payment.mode = self._random_payment_mode()

        if secrets.choice([True, False]):
            new_payment.note = fake.paragraph()

        if secrets.choice([True, False]):
            new_payment.payment_reference = fake.catch_phrase()

        new_payment.date = appointment.date
        new_payment.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"New Payment successfully bootstrapped: {new_payment} across patient {new_payment.patient}"
            )
        )

        self.stdout.write(self.style.SUCCESS("\n"))

    def _create_ad_hoc_payments(self):
        appointments_with_payment_made = Payment.objects.values_list(
            "appointment_id", flat=True
        )

        appointments_without_payment = Appointment.objects.exclude(
            id__in=appointments_with_payment_made
        )

        appointments_without_payment_and_present = appointments_without_payment.filter(
            state__title=APPOINTMENT_PRESENT_STATE_TITLE
        )

        for appointment in appointments_without_payment_and_present:
            self._create_payment(appointment=appointment)

        self.stdout.write(self.style.SUCCESS("\n"))


def clean_finance_app_data():

    print(Payment.objects.all().delete())
    print(Credit.objects.all().delete())
    print(PaymentMode.objects.all().delete())
