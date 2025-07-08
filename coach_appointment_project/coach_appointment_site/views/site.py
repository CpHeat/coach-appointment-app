from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.shortcuts import render

from ..decorators import group_required
from ..models import Appointment


@group_required([])
def dashboard_view(request):
    user = request.user

    if user.groups.filter(name='admin').exists():
        appointments = Appointment.objects.all()
        return render(request, "coach_appointment_site/dashboard.html", {'appointments': appointments})

    elif user.groups.filter(name='coach').exists():
        appointments = Appointment.objects.filter(coach=user)

        customers = User.objects.filter(
            appointments_customer__coach=user
        ).prefetch_related(
            Prefetch(
                'appointments_customer',
                queryset=Appointment.objects.filter(coach=user)
            )
        ).distinct()

        return render(request, "coach_appointment_site/dashboard.html",{'appointments': appointments, 'customers': customers})

    elif user.groups.filter(name='customer').exists():
        appointments = Appointment.objects.filter(customer=user)
        coaches = Appointment.objects.filter(customer=user).values_list('coach', flat=True).distinct()
        return render(request, "coach_appointment_site/dashboard.html",{'appointments': appointments, 'coaches': coaches})



def index_view(request):
    return render(request, "coach_appointment_site/index.html", {})