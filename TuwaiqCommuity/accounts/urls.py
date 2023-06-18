from django.urls import path
from . import views

app_name= "accounts"

urlpatterns =[
    path('signup/',views.sign_up,name="sign_up"),
    path('login/',views.login_page,name="login_page"),
    path('',views.log_out,name="log_out"),
    path('profile/',views.profile, name="profile"),
  
    path('request/',views.signup_requests,name="signup_requests"),
    path('request/approve/<user_id>/',views.approve_signup, name='approve_signup'),
    path('request/reject/<user_id>/', views.reject_signup, name='reject_signup'),

    path('Waiting_list/', views.waiting_list, name="waiting_list"),


]