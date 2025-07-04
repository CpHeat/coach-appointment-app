from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect

@login_required(login_url="/login/")
def index(request):
    return render(request, "coach_appointment_site/index.html", {})

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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