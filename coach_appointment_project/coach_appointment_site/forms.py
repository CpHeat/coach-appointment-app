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
        initial=Group.objects.get(name="client").id
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email", "group")

class AppointmentCreationForm(ModelForm):
    date = forms.DateField(
        input_formats=['%m/%d/%Y'],
        widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(
        widget=forms.TimeInput(
            format='%H:%M',
            attrs={'type': 'time', 'step': '60'}),
            input_formats = ['%H:%M']
        )

    class Meta:
        model = Appointment
        fields = ("coach", "client", "date", "time", "subject")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        coach_group = Group.objects.get(name='coach')
        self.fields['coach'].queryset = User.objects.filter(groups=coach_group)

        client_group = Group.objects.get(name='client')
        self.fields['client'].queryset = User.objects.filter(groups=client_group)

        # Potential hours
        _hours = [
            (f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}")
            for h in range(8, 19)
            for m in (0, 30)
        ]
        self.fields['time'].choices = _hours