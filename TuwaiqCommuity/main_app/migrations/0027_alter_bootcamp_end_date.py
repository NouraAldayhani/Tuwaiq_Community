# Generated by Django 4.2.1 on 2023-06-21 11:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0026_alter_bootcamp_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bootcamp',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 21, 11, 45, 13, 455682, tzinfo=datetime.timezone.utc)),
        ),
    ]
