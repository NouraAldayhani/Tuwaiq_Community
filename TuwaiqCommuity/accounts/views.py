
from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Bootcamp

# Create your views here.
def login_page(request:HttpRequest):
        msg = None
            
            
        try:

                if request.method == "POST":
                    user : User = authenticate(request, Email=request.POST["Email"], password=request.POST["Password"])
                    if user:
                        login(request, user)
                        return redirect("main_app:home")
                    else:
                        msg = "Incorrect Credentials"
        except:
            msg = "Please choose another username!"
        return render(request, "accounts/login.html")


def profile(request:HttpRequest):
    return render(request,'accounts/profile.html')
