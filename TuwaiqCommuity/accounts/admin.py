from django.contrib import admin
from .models import Bootcamp, Profile, Project

# Register your models here.

class BootcampAdmin(admin.ModelAdmin):
    list_display=('name','category','is_active')
    list_filter=('category',)

class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','bootcamp')
    list_filter=('bootcamp',)


admin.site.register(Bootcamp,BootcampAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Project)

