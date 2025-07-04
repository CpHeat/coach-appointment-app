from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import ModelForm

from .models import Appointment


class CustomUserCreationForm(UserCreationForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=["admin", "client", "coach"]),
        required=True,
        widget=forms.Select,
        initial=Group.objects.get(name="coach").id
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "group")

class AppointmentCreationForm(ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'step': '60'}))

    class Meta:
        model = Appointment
        fields = ("date", "time", "coach", "client", "appointment_subject")