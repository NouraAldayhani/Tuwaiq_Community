from django.urls import path
from . import views

app_name= "main_app"

urlpatterns=[
    path('',views.welcome_page,name="welcome_page"),
    path('home/',views.home_page,name="home_page"),
    path('about/',views.about_page,name="about_page"),
    path("contact/", views.add_contact, name = "contact"),
    path("bootcamps/search/", views.search_page, name="search_page"),

#Bootcamp
    path('create/bootcamp/',views.create_bootcamp, name="create_bootcamp"),
    path('bootcamps/',views.bootcamps_page, name="bootcamps"),
    path('bootcamps/<category>',views.category_bootcamps, name="category_bootcamps"),
    path('update/bootcamp/<bootcamp_id>/',views.update_bootcamp, name="update_bootcamp"),
    path('delete/bootcamp/<bootcamp_id>/',views.delete_bootcamp, name="delete_bootcamp"),
    path('bootcamp/<bootcamp_id>/',views.bootcamp_page,name="bootcamp_page"),
    path('activate/bootcamp/<bootcamp_id>/',views.is_active_bootcamp,name="is_active_bootcamp"),

#Question
    path('bootcamp/<bootcamp_id>/add_question/', views.update_question, name='add_question'),
    path('bootcamp/<bootcamp_id>/update_question/<question_id>/', views.update_question, name='update_question'),
    path('bootcamp/<bootcamp_id>/delete_question/<question_id>/', views.delete_question, name='delete_question'),
    path('bootcamp/<bootcamp_id>/delete_all_questions/', views.delete_all_questions, name='delete_all_questions'),

#Reply
    path('reply/detail/<question_id>/',views.reply_detail,name="reply_detail"),
    path('add/reply/<question_id>/',views.add_reply,name="add_reply"),
    path('update/reply/<reply_id>/',views.update_reply,name="update_reply"),
    path('delete/reply/<reply_id>/',views.delete_reply,name="delete_reply"),

#Event
    path('events/',views.events,name="events"),
    path('bootcamp/event/<bootcamp_id>/',views.bootcamp_event,name="bootcamp_event"),
    path('create/event/<bootcamp_id>/',views.create_event,name="create_event"),
    path('event/details/<event_id>/',views.event_details,name="event_details"),
    path('delete/event/<event_id>/',views.delete_event,name="delete_event"),
    path('update/event/<event_id>/',views.update_event,name="update_event"),

#notification
    path('notifications/', views.notification_view, name='notification_view'),
    path('delete_notification/', views.delete_notification, name='delete-notification'),
]
