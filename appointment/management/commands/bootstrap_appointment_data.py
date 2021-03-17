import datetime
import secrets

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker

from appointment.models import Appointment, FollowUp, State, TimeSlot
from patient.models import Patient
from staff.models import Staff

fake = Faker("en_IN")


class Command(BaseCommand):
    help = "Bootstrapping Appointment Data"

    def add_arguments(self, parser):
        pass

    @transaction.atomic()
    def handle(self, *args, **options):

        self._raise_error_if_staff_data_not_bootstrapped()
        self._raise_error_if_patient_data_not_bootstrapped()

        self._create_timeslots()

        self._create_states()

        self._create_appointments(total_appointments=50, back_date=3)

        self._mark_appointments_as_present(appointments=25)

        self._create_follow_ups(appointments=23)

        # self._flag_follow_ups(appointments=10)

        self.stdout.write(
            self.style.SUCCESS("Appointment Data successfully bootstrapped")
        )

    def _create_timeslots(self):
        all_timeslots = [
            {
                "title": "Morning",
                "start_time": datetime.time(hour=7),
                "end_time": datetime.time(hour=10),
            },
            {
                "title": "Afternoon",
                "start_time": datetime.time(hour=10),
                "end_time": datetime.time(hour=13),
            },
            {
                "title": "Evening",
                "start_time": datetime.time(hour=15),
                "end_time": datetime.time(hour=18),
            },
            {
                "title": "Night",
                "start_time": datetime.time(hour=18),
                "end_time": datetime.time(hour=21),
            },
        ]

        su = Staff.objects.get(id__username="SuperUser")

        for timeslot in all_timeslots:
            new_timeslot = TimeSlot()
            new_timeslot.title = timeslot["title"]
            new_timeslot.start_time = timeslot["start_time"]
            new_timeslot.end_time = timeslot["end_time"]
            new_timeslot.created_by = new_timeslot.updated_by = su
            new_timeslot.save()

            self.stdout.write(
                self.style.SUCCESS(f"Timeslot successfully bootstrapped: {timeslot}")
            )

        self.stdout.write(self.style.SUCCESS("\n"))

    def _create_states(self):
        states = [
            "Scheduled",
            "Present",
            "Absent",
            "Follow Up Registered",
            "Follow Up Pending",
            "Follow Up Done",
            "Rescheduled",
        ]

        su = Staff.objects.get(id__username="SuperUser")

        for state in states:
            new_state = State()
            new_state.title = state
            new_state.created_by = new_state.updated_by = su
            new_state.save()

            self.stdout.write(
                self.style.SUCCESS(f"State successfully bootstrapped: {new_state}")
            )

        self.stdout.write(self.style.SUCCESS("\n"))

    @staticmethod
    def _fetch_random_staff() -> Staff:
        return Staff.objects.active().order_by("?").first()

    @staticmethod
    def _fetch_random_patient() -> Patient:
        return Patient.objects.all().order_by("?").first()

    @staticmethod
    def _fetch_random_timeslot() -> TimeSlot:
        return TimeSlot.objects.all().order_by("?").first()

    @staticmethod
    def _fetch_random_back_date(back_date: int) -> datetime.date:

        back_date_days = back_date * 30
        random_number = secrets.randbelow(back_date_days)
        generated_date = datetime.datetime.today() - datetime.timedelta(
            days=random_number
        )
        return generated_date.date()

    @staticmethod
    def _fetch_random_future_date(future_date: int) -> datetime.date:

        future_date_days = future_date * 30
        random_number = secrets.randbelow(future_date_days)
        generated_date = datetime.datetime.today() + datetime.timedelta(
            days=random_number
        )
        return generated_date.date()

    def _create_appointments(self, total_appointments: int, back_date: int):

        for i in range(1, total_appointments):

            random_appointment_date = self._fetch_random_back_date(back_date=back_date)
            random_staff = self._fetch_random_staff()
            random_patient = self._fetch_random_patient()
            random_timeslot = self._fetch_random_timeslot()
            scheduled_state = State.objects.get(slug="scheduled")

            new_appointment = Appointment()
            new_appointment.patient = random_patient
            new_appointment.date = random_appointment_date
            new_appointment.staff = random_staff
            new_appointment.timeslot = random_timeslot
            new_appointment.state = scheduled_state

            new_appointment.created_by = new_appointment.updated_by = random_staff

            new_appointment.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Appointment successfully bootstrapped: {new_appointment}"
                )
            )

        self.stdout.write(self.style.SUCCESS("\n"))

    def _mark_appointments_as_present(self, appointments):

        present_state = State.objects.get(slug="present")

        for i in range(1, appointments + 1):
            appointment = (
                Appointment.objects.filter(state__slug="scheduled")
                .order_by("?")
                .first()
            )
            appointment.state = present_state
            appointment.updated_by = self._fetch_random_staff()
            appointment.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Appointment successfully marked as present: {appointment}"
                )
            )

        self.stdout.write(self.style.SUCCESS("\n"))

    def _create_follow_ups(self, appointments: int):

        rescheduled = State.objects.get(slug="rescheduled")
        absent_state = State.objects.get(slug="absent")
        follow_up_pending = State.objects.get(slug="follow-up-pending")
        follow_up_done = State.objects.get(slug="follow-up-done")
        follow_up_registered = State.objects.get(slug="follow-up-registered")

        for i in range(1, appointments + 1):

            # assign staff for operation
            staff = self._fetch_random_staff()

            # mark scheduled appointment as absent
            scheduled_appointment = (
                Appointment.objects.filter(state__slug="scheduled")
                .order_by("?")
                .first()
            )
            scheduled_appointment.state = absent_state
            scheduled_appointment.updated_by = staff
            scheduled_appointment.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Appointment marked absent: {scheduled_appointment}"
                )
            )

            # create followup pending
            followup = FollowUp()
            followup.original_appointment = scheduled_appointment
            followup.state = follow_up_pending
            followup.created_by = followup.updated_by = staff
            followup.save()

            self.stdout.write(self.style.SUCCESS(f"Follow up created : {followup}"))

            # mark appointment as followup follow_up_registered
            scheduled_appointment.state = follow_up_registered
            scheduled_appointment.updated_by = staff
            scheduled_appointment.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Appointment marked followup registered: {scheduled_appointment}"
                )
            )

            # create new rescheduled appointment from followup as output of followup
            new_appointment = Appointment()
            new_appointment.patient = scheduled_appointment.patient
            new_appointment.date = self._fetch_random_future_date(future_date=1)
            new_appointment.staff = scheduled_appointment.staff
            new_appointment.timeslot = scheduled_appointment.timeslot
            new_appointment.state = rescheduled

            new_appointment.created_by = new_appointment.updated_by = staff
            new_appointment.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"New Rescheduled Appointment created: {new_appointment}"
                )
            )

            # attach new appointment to follow up
            followup.new_appointment = new_appointment
            followup.state = follow_up_done
            followup.updated_by = staff
            followup.save()

            self.stdout.write(
                self.style.SUCCESS(f"Follow up marked as done: {followup}")
            )

        self.stdout.write(self.style.SUCCESS("\n"))

    @staticmethod
    def _flag_follow_ups(appointments):
        pass

    @staticmethod
    def _raise_error_if_staff_data_not_bootstrapped():
        staff_data_exists = Staff.objects.active().exists()
        if not staff_data_exists:
            raise CommandError("Please bootstrap Staff Data")

    @staticmethod
    def _raise_error_if_patient_data_not_bootstrapped():
        patient_data_exists = Patient.objects.all().count()
        if not patient_data_exists:
            raise CommandError("Please bootstrap Patient Data")
