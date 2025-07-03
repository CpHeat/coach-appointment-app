from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.auth_view, name="auth_view"),
    path("accounts/", include("django.contrib.auth.urls")),
] + debug_toolbar_urls()