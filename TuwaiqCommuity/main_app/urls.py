from django.urls import path
from . import views

app_name= "main_app"

urlpatterns=[
    path('',views.welcome_page,name="welcome_page"),
    path('home/',views.home_page,name="home_page"),
    path('create/bootcamp/',views.create_bootcamp, name="create_bootcamp"),
    path('bootcamps/',views.bootcamps_page, name="bootcamps"),
    path('mybootcamp/',views.my_bootcamp_page,name="my_bootcamp_page"),
    path('bootcamp/event',views.bootcamp_event,name="bootcamp_event"),
    path('event/details',views.event_details,name="event_details"),
]
