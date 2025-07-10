import datetime

from django.contrib.auth.models import User
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