from debug_toolbar.toolbar import debug_toolbar_urls
from django.urls import path

from . import views


urlpatterns = [
    path('access-denied/<str:required_role>/', views.access_denied_view, name='access_denied'),
    path("signup/", views.signup_view, name="signup"),
    path("signup/success", views.signup_success_view, name="signup_success"),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("", views.index_view, name="index"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("user/create/", views.create_user_view, name="create_user"),
    path("appointment/<int:appointment_id>/add-note/", views.add_appointment_note_view, name="add_appointment_note"),
    path("appointment/<int:appointment_id>/delete/", views.delete_appointment_view, name="delete_appointment"),
    path("profile/update/", views.update_profile_view, name="update_profile"),
    path("profile/", views.profile_view, name="profile"),
    path("coaches/", views.coaches_view, name="coaches"),
] + debug_toolbar_urls()