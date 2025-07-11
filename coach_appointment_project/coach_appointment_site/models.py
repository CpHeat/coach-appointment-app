import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CheckConstraint, Q
from django.db.models.signals import post_save
from django.dispatch import receiver


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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    avatar = models.CharField(max_length=50, null=True, blank=True)
    discipline = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s profile"

    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.profile.save()