from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path

from . import views


urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.index_view, name="index"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("create_user/", views.create_user_view, name="create_user"),
    path("create_appointment/", views.create_appointment_view, name="create_appointment"),
] + debug_toolbar_urls()