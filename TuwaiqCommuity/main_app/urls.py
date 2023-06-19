from django.urls import path
from . import views

app_name= "main_app"

urlpatterns=[
    path('',views.welcome_page,name="welcome_page"),
    path('home/',views.home_page,name="home_page"),
    path('create/bootcamp/',views.create_bootcamp, name="create_bootcamp"),
    path('bootcamps/',views.bootcamps_page, name="bootcamps"),
  
    path('bootcamp/<bootcamp_id>/',views.bootcamp_page,name="bootcamp_page"),
    path('add/question/<bootcamp_id>/',views.add_question,name="add_question"),
    path('reply/detail/<question_id>/',views.rply_detail,name="rply_detail"),

    path('bootcamp/event/<bootcamp_id>/',views.bootcamp_event,name="bootcamp_event"),
    path('create/event/<bootcamp_id>/',views.create_event,name="create_event"),
    path('event/details/<event_id>/',views.event_details,name="event_details"),
    path('delete/event/<event_id>/',views.delete_event,name="delete_event"),

    path('about/',views.about_page,name="about_page"),
    path('project/details/',views.project_details,name="project_details"), 
    path("contact/", views.add_contact, name = "contact"),

]
