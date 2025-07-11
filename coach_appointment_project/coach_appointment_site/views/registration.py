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
    if request.user.is_authenticated:
        return redirect('coach_appointment_site:dashboard')
    customer_group, created = Group.objects.get_or_create(name='customer')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            # Saves the user as inactive and attach it to customer group
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.groups.add(customer_group)

            # Sends the confirmation mail
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('emails/account_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return redirect("coach_appointment_site:signup_success")
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form, "customer_group": customer_group})

def signup_success_view(request):
    if request.user.is_authenticated:
        return redirect('coach_appointment_site:dashboard')
    return render(request,'registration/signup_success.html')

def activate_account(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect('coach_appointment_site:dashboard')
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
    if request.user.is_authenticated:
        return redirect('coach_appointment_site:dashboard')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("coach_appointment_site:dashboard")
        else:
            print("erreurs:", form.errors)
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})

@group_required()
def logout_view(request):
    logout(request)
    return redirect("coach_appointment_site:index")