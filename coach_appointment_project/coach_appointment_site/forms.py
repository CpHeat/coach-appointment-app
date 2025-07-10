import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils import timezone

from .models import Appointment, Profile


class CustomUserCreationForm(UserCreationForm):
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=["admin", "customer", "coach"]),
        required=True,
        widget=forms.Select,
        initial=Group.objects.get(name="customer").id
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name", "email", "group")

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        errors = {}

        if User.objects.filter(email=email).exists():
            errors["email"] = "This email is already registered."
        if User.objects.filter(username=username).exists():
            errors["username"] = "This username is already registered."
        if errors:
            raise ValidationError(errors)
        return cleaned_data

class AppointmentCreationForm(ModelForm):
    date = forms.DateField(
        initial=timezone.now().date,
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
        fields = ("coach", "customer", "date", "time", "subject")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        coach_group = Group.objects.get(name='coach')
        self.fields['coach'].queryset = User.objects.filter(groups=coach_group)

        customer_group = Group.objects.get(name='customer')
        self.fields['customer'].queryset = User.objects.filter(groups=customer_group)

        # Potential hours
        _hours = [
            (f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}")
            for h in range(8, 19)
            for m in (0, 30)
        ]
        self.fields['time'].choices = _hours

    def clean(self):
        cleaned_data = super().clean()
        coach = cleaned_data.get('coach')
        customer = cleaned_data.get('customer')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if coach and not coach.groups.filter(name='coach').exists():
            self.add_error('coach', 'This user is not in group coach.')

        if time and (time < datetime.time(8, 0) or time > datetime.time(19, 0)):
            self.add_error('time', 'Appointment time must be between 8h00 and 18h30.')

        if date:
            if date.weekday() == 6:
                self.add_error('date', 'Appointments can\'t be taken on Sundays.')
            elif date < timezone.now().date():
                self.add_error('date', 'Appointments must be in the future.')
            elif date == timezone.now().date() and time and time < timezone.now().time():
                self.add_error('time', 'Appointments must be in the future.')

        if coach and date and time:
            clash = Appointment.objects.filter(
                coach=coach,
                date=date,
                time=time
            )
            if self.instance.pk:
                clash = clash.exclude(pk=self.instance.pk)
            if clash.exists():
                self.add_error('coach', f"{coach.first_name} {coach.last_name} already has an appointment at this date and time.")

        if customer and date and time:
            clash = Appointment.objects.filter(
                customer=customer,
                date=date,
                time=time
            )
            if self.instance.pk:
                clash = clash.exclude(pk=self.instance.pk)
            if clash.exists():
                self.add_error('customer', f"{customer.first_name} {customer.last_name} already has an appointment at this date and time.")

        return cleaned_data

class AppointmentNoteForm(ModelForm):
    class Meta:
        model = Appointment
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Add or update your notes here...'
            }),
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'discipline']