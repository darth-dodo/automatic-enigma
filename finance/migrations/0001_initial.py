# Generated by Django 3.1.7 on 2021-03-17 07:44

import django.core.validators
import django.db.models.deletion
import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("staff", "0001_initial"),
        ("appointment", "0001_initial"),
        ("patient", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Credit",
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
                ("valid_until", models.DateField()),
                (
                    "total_amount",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "balance",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="credit_created_by",
                        to="staff.staff",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="credits",
                        to="patient.patient",
                    ),
                ),
            ],
            options={
                "ordering": ["-modified"],
            },
        ),
        migrations.CreateModel(
            name="PaymentMode",
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
                        related_name="paymentmode_created_by",
                        to="staff.staff",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="paymentmode_updated_by",
                        to="staff.staff",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
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
                (
                    "amount",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("payment_reference", models.TextField(blank=True, null=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "appointment",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payments",
                        to="appointment.appointment",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payment_created_by",
                        to="staff.staff",
                    ),
                ),
                (
                    "credit",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="finance.credit",
                    ),
                ),
                (
                    "mode",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="finance.paymentmode",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payments",
                        to="patient.patient",
                    ),
                ),
                (
                    "staff",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payments",
                        to="staff.staff",
                    ),
                ),
                (
                    "timeslot",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payments",
                        to="appointment.timeslot",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        limit_choices_to={"status": 1},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payment_updated_by",
                        to="staff.staff",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="credit",
            name="payment_mode",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="credits",
                to="finance.paymentmode",
            ),
        ),
        migrations.AddField(
            model_name="credit",
            name="updated_by",
            field=models.ForeignKey(
                limit_choices_to={"status": 1},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="credit_updated_by",
                to="staff.staff",
            ),
        ),
    ]