from django.contrib import admin

from .models import Appointment


class AppointmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date information', {'fields': ['date', 'time'], "classes": ["collapse"]}),
        ('Users', {'fields': ['coach', 'client'], "classes": ["collapse"]}),
        (None, {'fields': ['subject', 'note', 'attended']}),
    ]
    list_display = ('subject', 'note', 'attended', 'date', 'time', 'client', 'coach')
    list_filter = ["date", "coach"]
    search_fields = ['subject']

admin.site.register(Appointment, AppointmentAdmin)
