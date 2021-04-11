import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
    TitleSlugDescriptionModel,
)
from simple_history.models import HistoricalRecords

from finance.constants import APPOINTMENT_PRESENT_STATE_TITLE

"""
### Finance
- payment modes
- payment is across appointment
- payment can have payment modes
- payment has a reference
- payment can be from patient credit

"""

# Abstract Models


class FinanceHistoricalRecordMixin(models.Model):
    """
    Abstract model for integrating Historical Records/ Record versioning in shadow tables
    """

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class FinanceAbstractModel(TimeStampedModel, FinanceHistoricalRecordMixin):
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


class PaymentMode(FinanceAbstractModel, TitleSlugDescriptionModel):
    pass

    class Meta:
        unique_together = ["title"]

    def __str__(self) -> str:
        return f"{self.title}"


class Credit(FinanceAbstractModel):
    valid_until = models.DateField()
    total_amount = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    balance = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    patient = models.ForeignKey(
        to="patient.Patient", on_delete=models.PROTECT, related_name="credits"
    )
    payment_mode = models.ForeignKey(
        to="finance.PaymentMode", on_delete=models.PROTECT, related_name="credits"
    )
    notes = models.TextField(blank=True, null=True)

    def clean(self):

        if not self.pk:
            self.balance = self.total_amount

        if self.balance > self.total_amount:
            raise ValidationError("Balance amount cannot be more Total Amount!")

        today = datetime.datetime.today().date()

        if self.valid_until < today:
            raise ValidationError("Validity expired")

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return f"Patient: {self.patient} Total: {self.total_amount} Balance: {self.balance}"


class Payment(FinanceAbstractModel):

    # redundant fks derived from appointment for lesser db hops
    patient = models.ForeignKey(
        to="patient.Patient",
        null=True,
        blank=True,
        related_name="payments",
        on_delete=models.PROTECT,
    )
    staff = models.ForeignKey(
        to="staff.Staff",
        null=True,
        blank=True,
        related_name="payments",
        on_delete=models.PROTECT,
    )
    timeslot = models.ForeignKey(
        to="appointment.TimeSlot",
        null=True,
        blank=True,
        related_name="payments",
        on_delete=models.PROTECT,
    )

    appointment = models.OneToOneField(
        to="appointment.Appointment", related_name="payments", on_delete=models.PROTECT
    )
    date = models.DateField()

    credit = models.ForeignKey(
        to="finance.Credit", null=True, blank=True, on_delete=models.PROTECT
    )
    mode = models.ForeignKey(to="finance.PaymentMode", on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    payment_reference = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def clean(self):

        if self.appointment.state.title != APPOINTMENT_PRESENT_STATE_TITLE:
            raise ValidationError(
                "Payment cannot be registered across appointment which is not marked as Present!"
            )

        self.patient = self.appointment.patient
        self.staff = self.appointment.staff
        self.timeslot = self.appointment.timeslot

    class Meta:
        unique_together = ["appointment", "patient"]

    def save(self, *args, **kwargs):

        if not self.pk:
            self.patient = self.appointment.patient
            self.staff = self.appointment.staff
            self.timeslot = self.appointment.timeslot

        super().save(*args, **kwargs)
        if self.credit:
            self._update_credit_balance()

    def _update_credit_balance(self):
        credit_object = self.credit
        credit_object.balance -= self.amount
        credit_object.save()

    @property
    def is_from_credit(self) -> bool:
        return True if self.credit else False

    @property
    def is_from_credit_verbose(self) -> str:
        return "Yes" if self.is_from_credit else "NA"

    def __str__(self) -> str:
        return f"Payment for Patient {self.patient} Staff: {self.staff} Amount: {self.amount} Credit: {self.is_from_credit_verbose}"
