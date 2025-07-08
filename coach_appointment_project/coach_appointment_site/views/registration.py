from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from ..decorators import group_required
from ..forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from ..tokens import account_activation_token


def access_denied_view(request, required_role=None):
    return render(
        request,
        'registration/custom_access_denied.html',
        {"required_role": required_role})

def signup_view(request):
    client_group, created = Group.objects.get_or_create(name='client')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Saves the user as inactive and attach it to client group
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.groups.add(client_group)

            # Sends the confirmation mail
            current_site = get_current_site(request)
            mail_subject = 'Active ton compte.'
            message = render_to_string('registration/account_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return redirect("coach_appointment_site:login")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form, "client_group": client_group})

def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/activation_success.html')
    else:
        return render(request, 'registration/activation_invalid.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("connection active")
            login(request, user)
            return redirect("coach_appointment_site:index")

    return render(request, "registration/login.html", {"form": AuthenticationForm()})

@group_required()
def logout_view(request):
    logout(request)
    return redirect("coach_appointment_site:index")