# Generated by Django 3.1.7 on 2021-04-22 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("patient", "0003_auto_20210405_1716"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalpatient",
            name="locality",
            field=models.TextField(default="NA"),
        ),
        migrations.AddField(
            model_name="patient",
            name="locality",
            field=models.TextField(default="NA"),
        ),
    ]