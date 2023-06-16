from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Bootcamp,Profile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
# Create your views here.

def sign_up(request:HttpRequest):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bootcamp_name = request.POST.get('bootcamp_name')
        if not bootcamp_name:
            messages.error(request, 'Please select a bootcamp.')
            return redirect('accounts:sign_up')

        # Validate form data
        if not bootcamp_name:
            messages.error(request, 'Please select a bootcamp.')
            return redirect('accounts:sign_up')

        # Retrieve Bootcamp object from database
        bootcamp_qs = Bootcamp.objects.filter(name=bootcamp_name)
        if not bootcamp_qs.exists():
            messages.error(request, f'Bootcamp "{bootcamp_name}" does not exist.')
            return redirect('accounts:sign_up')
        bootcamp = bootcamp_qs.first()

        # Create User object
        user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)

        # Create Profile object
        profile = Profile(user=user, bootcamp=bootcamp)
        profile.save()
        messages.success(request, f'Your account request has been submitted for approval. Please wait for confirmation.')
        return redirect('accounts:login_page')
    else:
        bootcamps = Bootcamp.objects.all()
        return render(request, 'accounts/sign_up.html', { 'bootcamps': bootcamps })
    


def login_page(request:HttpRequest):
    msg = None
        
    if request.method == "POST":
        user : User = authenticate(request, username = request.POST["username"] , password = request.POST["password"])
        if user:
            login(request, user)
            return redirect("main_app:home_page")
        else:
            msg = "Incorrect Credentials"
      
    return render(request, "accounts/login.html", {"msg" : msg })


def log_out(request: HttpRequest):
    logout(request)
    return redirect("main_app:welcome_page")

      
def profile(request:HttpRequest):
    return render(request,'accounts/profile.html')
  

  
def request_page(request : HttpRequest):
    return render(request, "accounts/request.html")


