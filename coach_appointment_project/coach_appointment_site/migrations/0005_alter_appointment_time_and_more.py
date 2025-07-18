# Generated by Django 5.2.4 on 2025-07-07 12:17

import datetime
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coach_appointment_site', '0004_alter_appointment_time'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(default=django.utils.timezone.now, verbose_name='Appointment time'),
            preserve_default=False,
        ),
        migrations.AddConstraint(
            model_name='appointment',
            constraint=models.CheckConstraint(condition=models.Q(('date__gte', datetime.date(2025, 7, 7))), name='appointment_date_in_future'),
        ),
    ]
