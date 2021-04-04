# Create your models here.
from django.db import models
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
    TitleSlugDescriptionModel,
)

"""
### Appointments
- time slots are flexible
- appointment has a state
- appointment has a time slot
- appointment has a patient
- appointment has a staff
- appointment has several followups
- appointment has several appointment notes
"""


class AppointmentAbstractModel(TimeStampedModel):
    created_by = models.ForeignKey(
        to="staff.Staff",
        related_name="%(class)s_created_by",
        on_delete=models.PROTECT,
        limit_choices_to={"status": ActivatorModel.ACTIVE_STATUS},
    )

    updated_by = models.ForeignKey(
        to="staff.Staff",
        related_name="%(class)s_updated_by",
        on_delete=models.PROTECT,
        limit_choices_to={"status": ActivatorModel.ACTIVE_STATUS},
    )

    class Meta:
        abstract = True


class TimeSlot(AppointmentAbstractModel, TitleSlugDescriptionModel):
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ["title", "slug"]

    def __str__(self):
        return f"{self.title} - {self.start_time} - {self.end_time}"


class State(AppointmentAbstractModel, TitleSlugDescriptionModel):
    pass

    class Meta:
        unique_together = ["title", "slug"]

    def __str__(self):
        return f"{self.title}"


class Appointment(AppointmentAbstractModel):
    timeslot = models.ForeignKey(
        to="appointment.TimeSlot", on_delete=models.PROTECT, related_name="appointments"
    )
    date = models.DateField()

    patient = models.ForeignKey(
        "patient.Patient", on_delete=models.PROTECT, related_name="appointments"
    )
    staff = models.ForeignKey(
        "staff.Staff", on_delete=models.PROTECT, related_name="appointments"
    )

    state = models.ForeignKey(
        "appointment.State", on_delete=models.PROTECT, related_name="appointments"
    )

    notes = models.TextField(blank=True, null=True)

    reminder_sent = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date", "-modified"]

    @property
    def reminder_verbose(self):
        return "Yes" if self.reminder_sent else "No"

    def __str__(self):
        return (
            f"Patient: {self.patient.full_name} Staff: {self.staff.code} "
            f"Timeslot: {self.timeslot.title} State: {self.state.title} "
            f"Reminder Sent: {self.reminder_verbose}"
        )


class FollowUp(AppointmentAbstractModel):
    original_appointment = models.ForeignKey(
        "appointment.Appointment",
        on_delete=models.PROTECT,
        related_name="followups_inflow",
    )
    new_appointment = models.ForeignKey(
        "appointment.Appointment",
        on_delete=models.PROTECT,
        related_name="followups_outflow",
        null=True,
        blank=True,
    )
    state = models.ForeignKey(
        "appointment.State", on_delete=models.PROTECT, related_name="followups"
    )
    is_flagged = models.BooleanField(
        default=False
    )  # in case we need to escalate the followup
    notes = models.TextField(blank=True, null=True)

    def clean(self):
        if not self.new_appointment:
            return
        if not self.new_appointment.patient == self.original_appointment.patient:
            raise ValueError("Patient should be same for original and new appointment")

        if self.new_appointment.date <= self.original_appointment.date:
            raise ValueError(
                "New Appointment date cannot be before Old Appointment date"
            )

    class Meta:
        ordering = ["-modified"]

    @property
    def flagged_verbose(self):
        return "Y" if self.is_flagged else "N"

    def __str__(self):

        patient = f"Patient: {self.original_appointment.patient.full_name} "
        original_appointment = (
            f"Original Appointment Date: {self.original_appointment.date} "
        )
        if self.new_appointment:
            new_appointment = f"New Appointment Date: {self.new_appointment.date} "
        else:
            new_appointment = "New Appointment Date: Pending"

        return (
            f"{patient} {original_appointment} {new_appointment} "
            f"State: {self.state.title}"
            f"Flagged: {self.flagged_verbose}"
        )
