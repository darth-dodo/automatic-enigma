from django.core.validators import MinValueValidator
from django.db import models
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
    TitleSlugDescriptionModel,
)
from simple_history.models import HistoricalRecords

"""
### Treatment
- Difficulty
- Expertise
- Exercise Types
- Body Section is required for bucketing exercises based on different body parts
- Exercise has
    - Title
    - Exercise Type
    - Staff Expertise
    - Difficulty
    - multiple body sections
    - Information URL
    - Notes
- Exercise is from an exercise type
- An Exercise may impact multiple body parts
- Zero or more Equipment can be used in an exercise
- Regime is the recommended set/course of the Exercise attached to an appointment
- An Appointment can have one or more than exercises in it
"""


class TreatmentHistoricalRecordMixin(models.Model):
    """
    Abstract model for integrating Historical Records/ Record versioning in shadow tables
    """

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class TreatmentAbstractModel(TimeStampedModel, TreatmentHistoricalRecordMixin):
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


class Difficulty(TreatmentAbstractModel, TitleSlugDescriptionModel):
    pass

    class Meta:
        unique_together = ["title"]
        verbose_name_plural = "Difficulty"

    def __str__(self) -> str:
        return f"{self.title}"


class Expertise(TreatmentAbstractModel, TitleSlugDescriptionModel):
    pass

    class Meta:
        unique_together = ["title"]
        verbose_name_plural = "Expertise"

    def __str__(self) -> str:
        return f"{self.title}"


class ExerciseType(TreatmentAbstractModel, TitleSlugDescriptionModel):
    pass

    class Meta:
        unique_together = ["title"]

    def __str__(self) -> str:
        return f"{self.title}"


class BodySection(TreatmentAbstractModel, TitleSlugDescriptionModel):
    pass

    class Meta:
        unique_together = ["title"]

    def __str__(self) -> str:
        return f"{self.title}"


class Equipment(TreatmentAbstractModel, TitleSlugDescriptionModel):
    pass

    class Meta:
        unique_together = ["title"]

    def __str__(self) -> str:
        return f"{self.title}"


class Exercise(TreatmentAbstractModel, TitleSlugDescriptionModel):
    exercise_type = models.ForeignKey(
        to="treatment.ExerciseType", on_delete=models.PROTECT, related_name="exercises"
    )
    staff_expertise = models.ForeignKey(
        to="treatment.Expertise", on_delete=models.PROTECT, related_name="exercises"
    )
    difficulty = models.ForeignKey(
        to="treatment.Difficulty", on_delete=models.PROTECT, related_name="exercises"
    )
    body_sections = models.ManyToManyField(
        to="treatment.BodySection", related_name="exercises", blank=True
    )
    equipments = models.ManyToManyField(
        to="treatment.Equipment", related_name="exercises", blank=True
    )

    information_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["title"]

    def __str__(self) -> str:
        return f"{self.title}"


class Regime(TreatmentAbstractModel):
    daily_frequency = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_days = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    appointment = models.ForeignKey(
        to="appointment.Appointment",
        on_delete=models.PROTECT,
        related_name="exercise_regime",
    )
    patient = models.ForeignKey(
        to="patient.Patient",
        on_delete=models.PROTECT,
        related_name="exercise_regime",
        null=True,
        blank=True,
    )
    staff = models.ForeignKey(
        to="staff.Staff",
        on_delete=models.PROTECT,
        related_name="exercise_regime",
        null=True,
        blank=True,
    )
    exercise = models.ForeignKey(
        to="treatment.Exercise",
        on_delete=models.PROTECT,
        related_name="exercise_regime",
    )

    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ["appointment", "exercise"]
        verbose_name_plural = "Regime"

    def clean(self):

        self.patient = self.appointment.patient
        self.staff = self.appointment.staff

    def __str__(self) -> str:
        return f"{self.appointment} | {self.exercise}"

    def save(self, *args, **kwargs):

        if not self.pk:
            self.patient = self.appointment.patient
            self.staff = self.appointment.staff

        super().save(*args, **kwargs)
