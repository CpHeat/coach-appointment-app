import datetime
import random

from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.utils import timezone

from ..decorators import group_required
from ..forms import AppointmentCreationForm, AppointmentNoteForm
from ..models import Appointment


@group_required([])
def dashboard_view(request):
    user = request.user
    # Appointment form
    if request.method == "POST":
        form = AppointmentCreationForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)
            if request.user.groups.filter(name='coach').exists():
                appointment.coach = request.user
            elif request.user.groups.filter(name='customer').exists():
                appointment.customer = request.user
            appointment.save()
            return redirect("coach_appointment_site:dashboard")
        else:
            print(form.errors)
    else:
        form = AppointmentCreationForm(initial={'date': datetime.date.today()})

    # Dashboard
    if user.groups.filter(name='admin').exists():
        appointments = Appointment.objects.all()
        return render(request, "coach_appointment_site/dashboard.html", {'appointments': appointments})

    elif user.groups.filter(name='coach').exists():
        upcoming_appointments = [
            appointment for appointment in Appointment.objects.filter(coach=user).order_by('date', 'time')
            if timezone.make_aware(datetime.datetime.combine(appointment.date, appointment.time)) >= timezone.now()
        ]

        past_appointments = [
            appointment for appointment in Appointment.objects.filter(coach=user).order_by('date', 'time')
            if timezone.make_aware(datetime.datetime.combine(appointment.date, appointment.time)) < timezone.now()
        ]

        customers = User.objects.filter(
            appointments_customer__coach=user
        ).prefetch_related(
            Prefetch(
                'appointments_customer',
                queryset=Appointment.objects.filter(coach=user)
            )
        ).distinct()

        return render(request, "coach_appointment_site/dashboard.html",{'upcoming_appointments': upcoming_appointments, 'past_appointments': past_appointments, 'customers': customers, 'form': form})

    elif user.groups.filter(name='customer').exists():
        upcoming_appointments = [
            appointment for appointment in Appointment.objects.filter(customer=user)
            if timezone.make_aware(datetime.datetime.combine(appointment.date, appointment.time)) >= timezone.now()
        ]

        past_appointments = [
            appointment for appointment in Appointment.objects.filter(customer=user)
            if timezone.make_aware(datetime.datetime.combine(appointment.date, appointment.time)) < timezone.now()
        ]

        coaches = User.objects.filter(
            appointments_coach__customer=user
        ).prefetch_related(
            Prefetch(
                'appointments_coach',
                queryset=Appointment.objects.filter(customer=user)
            )
        ).distinct()

        return render(request, "coach_appointment_site/dashboard.html",{'upcoming_appointments': upcoming_appointments, 'past_appointments': past_appointments, 'coaches': coaches, 'form': form})

def index_view(request):
    return render(request, "coach_appointment_site/index.html", {})

@group_required([])
def profile_view(request):
    profile = request.user.profile
    return render(request, "coach_appointment_site/profile.html", {'profile': profile})

def coaches_view(request):
    coaches = User.objects.filter(groups__name='coach')
    return render(request, "coach_appointment_site/coaches.html", {"coaches": coaches})