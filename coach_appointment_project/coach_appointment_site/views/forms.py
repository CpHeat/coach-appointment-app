import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render, get_object_or_404

from ..decorators import group_required
from ..forms import AppointmentCreationForm, CustomUserCreationForm, AppointmentNoteForm, ProfileForm
from ..models import Appointment, Profile


@group_required(["admin"])
def create_user_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = form.cleaned_data["group"]
            user.groups.add(group)
            return redirect("coach_appointment_site:dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "coach_appointment_site/forms/create_user.html", {"form": form})

@group_required([])
def delete_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == "POST":
        appointment.delete()

        subject = "Appointment cancellation"
        message_customer = f"""
        Hello {appointment.customer.first_name} {appointment.customer.last_name},

        Your appointment with {appointment.coach.first_name} {appointment.coach.last_name} scheduled for the {appointment.date} at {appointment.time} has been cancelled.

        You can always reschedule an appointment through your dashboard.

        Yours truly,
        The Coach App team
        """
        message_coach = f"""
        Hello {appointment.coach.first_name} {appointment.coach.last_name},

        Your appointment with {appointment.customer.first_name} {appointment.customer.last_name} scheduled for the {appointment.date} at {appointment.time} has been cancelled.

        You can always reschedule an appointment through your dashboard.

        Yours truly,
        The Coach App team
        """

        send_mail(subject, message_customer, settings.DEFAULT_FROM_EMAIL, [appointment.customer.email])
        send_mail(subject, message_coach, settings.DEFAULT_FROM_EMAIL, [appointment.coach.email])

        return redirect("coach_appointment_site:dashboard")
    return redirect("coach_appointment_site:dashboard")

@group_required(["coach"])
def add_appointment_note_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if request.method == 'POST':
        form = AppointmentNoteForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('coach_appointment_site:dashboard')
    else:
        form = AppointmentNoteForm(instance=appointment)

    return render(request, 'coach_appointment_site/forms/add_appointment_note.html', {'form': form, 'appointment': appointment})

@group_required([])
def update_profile_view(request):
    profile, created = request.user.profile, False

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        print("form", form)

        if form.is_valid():
            form.save()
            return redirect('coach_appointment_site:dashboard')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'coach_appointment_site/forms/update_profile.html', {'form': form})