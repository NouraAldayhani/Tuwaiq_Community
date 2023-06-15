from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from main_app.models import Bootcamp
from django.http import HttpRequest, HttpResponse

# Create your views here.
def sign_up(request:HttpRequest):
    msg = None
    bootcamps=Bootcamp.objects.all()
    if request.method == "POST":
        try:
            bootcamp_name = bootcamps.name
            user = User.objects.create_user( first_name=request.POST["first_name"], last_name=request.POST["last_name"],email=request.POST["email"],bootcamp_name = request.POST['bootcamp_name'] ,password=request.POST["password"] )
            user.save()
            return redirect("main_app:home_page")# redirect (Waiting list) 
        except:
            msg = "Please choose another username!"

    return render(request, "accounts/sign_up.html", {"msg" : msg, "bootcamps":bootcamps})
