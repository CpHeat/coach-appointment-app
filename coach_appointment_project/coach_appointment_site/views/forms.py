import datetime

from django.shortcuts import redirect, render, get_object_or_404

from ..decorators import group_required
from ..forms import AppointmentCreationForm, CustomUserCreationForm
from ..models import Appointment

@group_required([])
def create_appointment_view(request):
    if request.method == "POST":
        form = AppointmentCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("coach_appointment_site:dashboard")
        else:
            print(form.errors)
    else:
        form = AppointmentCreationForm(initial={'date': datetime.date.today()})

    return render(request, "coach_appointment_site/forms/create_appointment.html", {"form": form})

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

@group_required([])
def update_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == "POST":
        form = AppointmentCreationForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect("coach_appointment_site:dashboard")
    else:
        form = AppointmentCreationForm(instance=appointment)
    return render(request, "coach_appointment_site/forms/update_appointment.html", {"form": form})