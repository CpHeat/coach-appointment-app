from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, AppointmentCreationForm


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Saves the user and attach it to client group
            user = form.save()
            client_group, created = Group.objects.get_or_create(name='client')
            user.groups.add(client_group)

            # Logs the user
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)

            return redirect("coach_appointment_site:login")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("coach_appointment_site:index")

    return render(request, "registration/login.html", {"form": AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect("coach_appointment_site:index")

def index_view(request):
    return render(request, "coach_appointment_site/index.html", {})

def dashboard_view(request):
    return render(request, "coach_appointment_site/dashboard.html", {})

def create_appointment_view(request):
    if request.method == "POST":
        form = AppointmentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("coach_appointment_site:dashboard")
    else:
        form = AppointmentCreationForm()
    return render(request, "coach_appointment_site/forms/create_appointment.html", {"form": form})

def create_user_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data["group"]
            user.groups.add(group)
            return redirect("coach_appointment_site:dashboard")
    else:
        form = CustomUserCreationForm()
    return render(request, "coach_appointment_site/forms/create_user.html", {"form": form})