# Generated by Django 4.2.2 on 2023-06-16 18:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main_app", "0006_alter_bootcamp_end_date_alter_contactus_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bootcamp",
            name="end_date",
            field=models.DateField(
                default=datetime.datetime(
                    2023, 7, 16, 18, 11, 28, 129826, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="contactus",
            name="descripton",
            field=models.TextField(null=True),
        ),
    ]
