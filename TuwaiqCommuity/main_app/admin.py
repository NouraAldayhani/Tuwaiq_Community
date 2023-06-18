from django.contrib import admin
from .models import ContactUs, Event, Attendance

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display=('user','bootcamp','event_title')
    list_filter=('bootcamp',)

class AttendanceAdmin(admin.ModelAdmin):
    list_display=('user','event','timestamp')
    list_filter=('event',)

admin.site.register(ContactUs)
admin.site.register(Event,EventAdmin)
admin.site.register(Attendance,AttendanceAdmin)
