# Generated by Django 4.2.1 on 2023-06-21 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='proflie',
            new_name='profile',
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='images/user_default.png', upload_to='images/'),
        ),
    ]
