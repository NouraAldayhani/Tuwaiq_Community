from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def welcome_page(request:HttpRequest):
    return render(request,'main_app/welcome.html')
 
def home_page(request:HttpRequest):
    
    return render(request,'main_app/home.html')

