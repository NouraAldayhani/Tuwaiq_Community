from django.urls import path
from . import views

app_name= "accounts"

urlpatterns =[
    path('signup/',views.sign_up,name="sign_up"),
    path('login/',views.login_page,name="login_page"),
    path('',views.log_out,name="log_out"),
    path('profile/',views.profile, name="profile"),
    path('request/',views.request_page,name="request_page"),
    path('Waiting_list/', views.Waiting_list, name="Waiting_list"),
    path('event/',views.event,name="event_page"),

]