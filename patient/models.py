# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from patient.constants import GENDER_OPTIONS

# Abstract Models


class PatientHistoricalRecordMixin(models.Model):
    """
    Abstract model for integrating Historical Records/ Record versioning in shadow tables
    """

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class PatientAbstractModel(TimeStampedModel, PatientHistoricalRecordMixin):
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


class PhoneNumber(PatientAbstractModel):
    phone_number = PhoneNumberField(unique=True)
    is_primary = models.BooleanField(default=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        pass

    @property
    def primary_phone_number(self):
        return "Primary" if self.is_primary else "Non Primary"

    def __str__(self):
        return f"{self.phone_number} - {self.primary_phone_number}"


class Patient(PatientAbstractModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=20, choices=GENDER_OPTIONS, default=GENDER_OPTIONS.undisclosed
    )

    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

    joining_date = models.DateField()
    primary_assessment_sheet = models.URLField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    primary_contact = models.ForeignKey(
        to="patient.PhoneNumber",
        related_name="primary_contacts",
        on_delete=models.PROTECT,
    )
    phone_numbers = models.ManyToManyField(
        to="patient.PhoneNumber", related_name="patients"
    )

    class Meta:
        unique_together = ["first_name", "last_name", "primary_contact"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name} - {self.gender} - {self.age}"


class PatientDetail(PatientAbstractModel):
    patient = models.OneToOneField(
        to="patient.Patient", related_name="detail", on_delete=models.PROTECT
    )
    is_referral = models.BooleanField(default=False)
    referred_by = models.ForeignKey(
        to="patient.Patient",
        null=True,
        blank=True,
        related_name="referrals",
        on_delete=models.PROTECT,
    )
    referral_notes = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)

    class Meta:
        pass

    @property
    def verbose_referral(self):
        return "Referral" if self.is_referral else "Non Referral"

    def __str__(self):
        return f"{self.patient} - {self.verbose_referral}"
