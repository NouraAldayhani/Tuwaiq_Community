from django.contrib import admin
from .models import ContactUs, Event, Attendance,Question,Reply

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display=('user','bootcamp','event_title')
    list_filter=('bootcamp',)

class AttendanceAdmin(admin.ModelAdmin):
    list_display=('user','event','timestamp')
    list_filter=('event',)

class QuestionAdmin(admin.ModelAdmin):
    list_display=('user','bootcamp','subject','timestamp')
    list_filter=('timestamp')

if not admin.site.is_registered(Question):
    class QuestionAdmin(admin.ModelAdmin):
        list_display=('user','bootcamp','subject','timestamp')
        list_filter=('timestamp',)
    admin.site.register(Question,QuestionAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display=('user','subject','timestamp')
    list_filter=('timestamp',)


if not admin.site.is_registered(Reply):
    admin.site.register(Reply)

admin.site.register(ContactUs)
admin.site.register(Event,EventAdmin)
admin.site.register(Attendance,AttendanceAdmin)
