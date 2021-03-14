from django.contrib.auth.models import User as CoreUser
from django.db import models
from django_extensions.db.models import (
    ActivatorModel,
    TimeStampedModel,
    TitleSlugDescriptionModel,
)

# Create your models here.


class CreatorMixin(models.Model):
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


class Role(
    TimeStampedAndActivatorModel, TitleSlugDescriptionModel, CreatorUpdaterMixin
):
    pass

    def __str__(self):
        return f"{self.title} - {self.slug} - {self.status}"


class Staff(TimeStampedAndActivatorModel, CreatorUpdaterMixin):
    id = models.OneToOneField(CoreUser, on_delete=models.PROTECT, primary_key=True)
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
        return f"{self.name} - {self.role}"


class Feedback(TimeStampedModel, CreatorUpdaterMixin):
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
