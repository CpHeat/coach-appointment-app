from django.contrib import admin

from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date information', {'fields': ['date', 'time'], "classes": ["collapse"]}),
        ('Users', {'fields': ['coach', 'client'], "classes": ["collapse"]}),
        (None, {'fields': ['appointment_subject']}),
    ]
    list_display = ('appointment_subject', 'date', 'time', 'client', 'coach')
    list_filter = ["date"]
    search_fields = ['appointment_subject']

admin.site.register(Appointment, AppointmentAdmin)
