from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class Appointment(models.Model):

    date = models.DateField('Appointment date')
    time = models.TimeField('Appointment time')
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_coach')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_client')
    appointment_subject = models.CharField(max_length=500)

    def clean(self):
        super().clean()
        if not self.coach.groups.filter(name='coach').exists():
            raise ValidationError({'coach': 'This user is not into group coach.'})