# Generated by Django 5.2.4 on 2025-07-08 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coach_appointment_site', '0017_appointment_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='avatar',
        ),
    ]
