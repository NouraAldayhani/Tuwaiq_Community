# Generated by Django 4.2.1 on 2023-06-21 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_merge_20230621_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type_project',
            field=models.CharField(choices=[('Unit Project', 'Unit Project'), ('Capstone Project', 'Capstone Project')], default='Unit Project', max_length=2000),
        ),
    ]
