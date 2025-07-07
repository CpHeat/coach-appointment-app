from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from ..decorators import group_required
from ..forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render


def access_denied_view(request, required_role=None):
    return render(
        request,
        'registration/custom_access_denied.html',
        {"required_role": required_role})

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

@group_required()
def logout_view(request):
    logout(request)
    return redirect("coach_appointment_site:index")