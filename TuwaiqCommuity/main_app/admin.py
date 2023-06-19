from django.contrib import admin
from .models import ContactUs, Event, Attendance,Question,Reply

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display=('user','bootcamp','event_title')
    list_filter=('bootcamp',)

class AttendanceAdmin(admin.ModelAdmin):
    list_display=('user','event','timestamp')
    list_filter=('event',)

if not admin.site.is_registered(Question):
    admin.site.register(Question)

if not admin.site.is_registered(Reply):
    admin.site.register(Reply)

admin.site.register(ContactUs)
admin.site.register(Event,EventAdmin)
admin.site.register(Attendance,AttendanceAdmin)
