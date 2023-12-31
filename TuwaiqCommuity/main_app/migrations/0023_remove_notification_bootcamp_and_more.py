# Generated by Django 4.2.2 on 2023-06-20 11:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_merge_20230620_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='bootcamp',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='event',
        ),
        migrations.AddField(
            model_name='notification',
            name='content',
            field=models.CharField(default='', max_length=2048),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bootcamp',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2023, 7, 20, 11, 30, 41, 572691, tzinfo=datetime.timezone.utc)),
        ),
    ]
