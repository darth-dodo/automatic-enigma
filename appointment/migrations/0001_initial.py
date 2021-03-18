# Generated by Django 3.1.7 on 2021-03-17 06:02

import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("staff", "0001_initial"),
        ("patient", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("date", models.DateField()),
                ("notes", models.TextField(blank=True, null=True)),
                ("reminder_sent", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="appointment_created_by",
                        to="staff.staff",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="appointments",
                        to="patient.patient",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="appointments",
                        to="staff.staff",
                    ),
                ),
            ],
            options={
                "ordering": ["-date", "-modified"],
            },
        ),
        migrations.CreateModel(
            name="TimeSlot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        populate_from="title",
                        verbose_name="slug",
                    ),
                ),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "created_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="timeslot_created_by",
                        to="staff.staff",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="timeslot_updated_by",
                        to="staff.staff",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="description"),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True,
                        editable=False,
                        populate_from="title",
                        verbose_name="slug",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="state_created_by",
                        to="staff.staff",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="state_updated_by",
                        to="staff.staff",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FollowUp",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    django_extensions.db.fields.ModificationDateTimeField(
                        auto_now=True, verbose_name="modified"
                    ),
                ),
                ("is_flagged", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="followup_created_by",
                        to="staff.staff",
                    ),
                ),
                (
                    "new_appointment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="followups_outflow",
                        to="appointment.appointment",
                    ),
                ),
                (
                    "original_appointment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="followups_inflow",
                        to="appointment.appointment",
                    ),
                ),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="followups",
                        to="appointment.state",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="followup_updated_by",
                        to="staff.staff",
                    ),
                ),
            ],
            options={
                "ordering": ["-modified"],
            },
        ),
        migrations.AddField(
            model_name="appointment",
            name="state",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="appointments",
                to="appointment.state",
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="timeslot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="appointments",
                to="appointment.timeslot",
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="updated_by",
            field=models.ForeignKey(
                limit_choices_to={"status": 1},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="appointment_updated_by",
                to="staff.staff",
            ),
        ),
    ]