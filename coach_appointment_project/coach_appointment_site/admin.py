from django.contrib import admin

from .models import Appointment, Profile


class AppointmentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Date information', {'fields': ['date', 'time'], "classes": ["collapse"]}),
        ('Users', {'fields': ['coach', 'customer'], "classes": ["collapse"]}),
        (None, {'fields': ['subject', 'note', 'attended']}),
    ]
    list_display = ('subject', 'note', 'attended', 'date', 'time', 'customer', 'coach')
    list_filter = ["date", "coach"]
    search_fields = ['subject']

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Profile)
