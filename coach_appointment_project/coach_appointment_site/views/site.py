from django.shortcuts import render

from ..decorators import group_required
from ..models import Appointment


@group_required([])
def dashboard_view(request):
    user = request.user

    if user.groups.filter(name='admin').exists():
        appointments = Appointment.objects.all()
    elif user.groups.filter(name='coach').exists():
        appointments = Appointment.objects.filter(coach=user)
    elif user.groups.filter(name='client').exists():
        appointments = Appointment.objects.filter(client=user)

    return render(request, "coach_appointment_site/dashboard.html", {'appointments': appointments})

def index_view(request):
    return render(request, "coach_appointment_site/index.html", {})