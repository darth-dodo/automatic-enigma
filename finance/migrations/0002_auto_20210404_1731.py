# Generated by Django 3.1.7 on 2021-04-04 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="paymentmode",
            unique_together={("title", "slug")},
        ),
    ]
