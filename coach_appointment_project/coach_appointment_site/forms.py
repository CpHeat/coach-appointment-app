from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from .models import Appointment


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