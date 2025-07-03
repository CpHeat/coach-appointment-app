from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def index(request):
    return render(request, "coach_appointment_site/index.html", {})

def auth_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("coach_appointment_site:login")
    else:
        return render(request, "registration/signup.html", {"form": UserCreationForm()})