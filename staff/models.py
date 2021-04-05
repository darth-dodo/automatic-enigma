from django.contrib.auth.models import User as CoreUser
from django.db import models
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
    TitleSlugDescriptionModel,
)
from simple_history.models import HistoricalRecords

# Abstract Models


class StaffHistoricalRecordMixin(models.Model):
    """
    Abstract model for integrating Historical Records/ Record versioning in shadow tables
    """

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class CreatorMixin(models.Model):
    """
    Abstract model for adding `created_by`
    """

    created_by = models.ForeignKey(
        "staff.Staff",
        related_name="%(class)s_created_by",
        on_delete=models.PROTECT,
        limit_choices_to={"status": ActivatorModel.ACTIVE_STATUS},
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class UpdaterMixin(models.Model):
    """
    Abstract model for adding `updated_by`
    """

    updated_by = models.ForeignKey(
        "staff.Staff",
        related_name="%(class)s_updated_by",
        on_delete=models.PROTECT,
        limit_choices_to={"status": ActivatorModel.ACTIVE_STATUS},
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class CreatorUpdaterMixin(CreatorMixin, UpdaterMixin):
    class Meta:
        abstract = True


class TimeStampedAndActivatorModel(TimeStampedModel, ActivatorModel):
    class Meta:
        abstract = True


# App Models


class Role(
    TimeStampedAndActivatorModel,
    TitleSlugDescriptionModel,
    CreatorUpdaterMixin,
    StaffHistoricalRecordMixin,
):
    """
    Model to store Staff roles eg. Finance, Senior Doctor, SuperUser

    This can be further used to restrict/grant access in combination with Django Groups or a new `Permissions` entity
    """

    class Meta:
        unique_together = ["title"]

    def __str__(self):
        return f"{self.title} - {self.slug} - {self.get_status_display()}"


class Staff(
    TimeStampedAndActivatorModel, CreatorUpdaterMixin, StaffHistoricalRecordMixin
):
    id = models.OneToOneField(
        CoreUser, on_delete=models.PROTECT, primary_key=True, related_name="staff"
    )
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=255)
    joining_date = models.DateField()
    role = models.ForeignKey(
        "staff.Role",
        on_delete=models.PROTECT,
        limit_choices_to={"status": ActivatorModel.ACTIVE_STATUS},
        null=True,
        blank=True,
    )
    supervisor = models.ForeignKey(
        "staff.Staff",
        blank=True,
        null=True,
        related_name="direct_reports",
        on_delete=models.PROTECT,
        limit_choices_to={"status": ActivatorModel.ACTIVE_STATUS},
    )

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.name} - {self.role.title} - {self.get_status_display()}"


class Feedback(TimeStampedModel, CreatorUpdaterMixin, StaffHistoricalRecordMixin):
    member = models.ForeignKey(
        to="staff.Staff",
        on_delete=models.PROTECT,
        limit_choices_to={"status": ActivatorModel.ACTIVE_STATUS},
    )
    text = models.TextField()

    class Meta:
        pass

    def __str__(self):
        return f"{self.member} - review by {self.created_by.name}"
