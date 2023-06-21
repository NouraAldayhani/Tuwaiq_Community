from django.urls import path
from . import views

app_name= "accounts"

urlpatterns =[
    path('signup/',views.sign_up,name="sign_up"),
    path('login/',views.login_page,name="login_page"),
    path('',views.log_out,name="log_out"),
    path('profile/<user_id>/',views.profile, name="profile"),
    path('update/profile/<user_id>/',views.update_profile, name="update_profile"),

  
    path('request/',views.signup_requests,name="signup_requests"),
    path('request/approve/<user_id>/',views.approve_signup, name='approve_signup'),
    path('request/reject/<user_id>/', views.reject_signup, name='reject_signup'),

    path('waitinglist/', views.waiting_list, name="waiting_list"),

    path('nopermission/',views.no_permission,name="no_permission"),

    path('bootCampsCategories/', views.bootCampsCategories, name="bootCampsCategories_page"),

    path('add/project/<user_id>/',views.add_project, name="add_project"),
    path('project/details/<project_id>',views.project_details,name="project_details"), 
    path('delete/project/<project_id>/',views.delete_project, name="delete_project"),
    path('update/project/<project_id>/',views.update_project, name="update_project"),

]