from django.urls import path
from . import views

app_name= "accounts"

urlpatterns=[
    path('request/',views.request_page,name="request_page"),
]