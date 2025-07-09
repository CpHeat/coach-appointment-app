import datetime

from django.contrib.auth.models import User, Group, AbstractUser
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.db import models
from django.db.models import CheckConstraint, Q

class Appointment(models.Model):

    date = models.DateField('Appointment date')
    time = models.TimeField('Appointment time')
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_coach')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_customer')
    subject = models.CharField(max_length=500)
    note = models.TextField(null=True, blank=True)
    attended = models.BooleanField(default=False)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(time__gte=datetime.time(8, 0)) & Q(time__lte=datetime.time(19, 0)),
                name='appointment_time_between_8_and_19'
            )
        ]

    def clean(self):
        super().clean()
        errors = {}

        if not self.coach.groups.filter(name='coach').exists():
            errors['coach'] = 'This user is not into group coach.'
        if self.time < datetime.time(8, 0) or self.time > datetime.time(19, 0):
            errors['time'] = 'Appointment time must be between 8h00 and 18h30.'
        if self.date.weekday() == 6:
            errors['date'] = 'Appointments can\'t be taken on sundays.'
        if self.date < datetime.date.today():
            errors['date'] = 'Appointments must be in the future.'
        elif self.date == datetime.date.today() and self.time < datetime.datetime.now().time():
            errors['time'] = 'Appointments must be in the future.'

        clash = Appointment.objects.filter(
            coach=self.coach,
            date=self.date,
            time=self.time
        )

        if self.pk:
            clash = clash.exclude(pk=self.pk)

        if clash.exists():
            errors.setdefault(NON_FIELD_ERRORS, []).append(
                f"{self.coach} already has an appointment at this date."
            )

        clash = Appointment.objects.filter(
            customer=self.customer,
            date=self.date,
            time=self.time
        )

        if self.pk:
            clash = clash.exclude(pk=self.pk)

        if clash.exists():
            errors.setdefault(NON_FIELD_ERRORS, []).append(
                f"{self.customer} already has an appointment at this date."
            )

        if errors:
            raise ValidationError(errors)