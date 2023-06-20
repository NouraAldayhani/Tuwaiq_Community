from django.contrib import admin
from .models import ContactUs, Event, Attendance,Question,Reply

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display=('user','bootcamp','event_title')
    list_filter=('bootcamp',)

class AttendanceAdmin(admin.ModelAdmin):
    list_display=('user','event','timestamp')
    list_filter=('event',)


#Questin
class QuestionAdmin(admin.ModelAdmin):
    list_display=('user','bootcamp','subject','timestamp')
    list_filter=('timestamp',)

if not admin.site.is_registered(Question):
    class QuestionAdmin(admin.ModelAdmin):
        list_display=('user','bootcamp','subject','timestamp')
        list_filter=('timestamp',)
    admin.site.register(Question,QuestionAdmin)

#Reply
class ReplyAdmin(admin.ModelAdmin):
        list_display=('user','subject','timestamp')
        list_filter=('timestamp',)

if not admin.site.is_registered(Reply):
    class ReplyAdmin(admin.ModelAdmin):
        list_display=('user','reply_description','timestamp')
        list_filter=('timestamp',)
    admin.site.register(Reply,ReplyAdmin)

admin.site.register(ContactUs)
admin.site.register(Event,EventAdmin)
admin.site.register(Attendance,AttendanceAdmin)
