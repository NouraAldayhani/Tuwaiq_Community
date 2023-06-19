from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Bootcamp,Profile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.

def sign_up(request:HttpRequest):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            bootcamp_name = request.POST.get('bootcamp_name')
            if not bootcamp_name:
                messages.error(request, 'Please select a bootcamp.')
                return redirect('accounts:sign_up')
        except:
                 messages.error(request, 'Please choose another username!')
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
        user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,is_active=False)

        # Create Profile object
        profile = Profile(user=user, bootcamp=bootcamp)
        profile.save()
        messages.success(request, f'Your account request has been submitted for approval. Please wait for confirmation.')
        return redirect('accounts:waiting_list')
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

@login_required
def profile(request:HttpRequest, user_id):
    try:
        profile = Profile.objects.get(user__id=user_id)
    except:
        return render(request, "main_app/not_found.html")
    return render(request, "accounts/profile.html", {"profile":profile})

@login_required
def update_profile(request:HttpRequest, user_id):
    #check permission
    if not (request.user.is_authenticated and request.user.id == int(user_id)):
        return redirect("accounts:no_permission")
    #check get or create profile
    try:
        user = User.objects.get(id=user_id)
        profile, is_created = Profile.objects.get_or_create(user=user)
    except:
        return render(request, "main_app/not_found.html")
    #update
    if request.method == "POST":
        profile.about_user = request.POST["about_user"]
        profile.github_link = request.POST["github_link"]
        profile.linkedin_link = request.POST["linkedin_link"]
        profile.twitter_link = request.POST["twitter_link"]
        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]
        profile.save()
        return redirect("accounts:profile", user_id=user_id)
    return render(request, "accounts/update_profile.html", {"profile":profile})
  
#views for signup_request.html  
def signup_requests(request : HttpRequest):
    #retrive inactive users and their bootcamp name
    inactive_users = User.objects.filter(is_active=False, is_staff=False).select_related('profile__bootcamp')
    num_requests = inactive_users.count()
    
    return render(request, "accounts/signup_requests.html", {"inactive_users":inactive_users, "num_requests":num_requests})

def approve_signup(request, user_id):
    #retrieve the user with the ID and activate user account
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()

    # #Send email activate notification to user
    subject = 'Your account has been activated'
    message = 'Dear {}, your account has been activated. You can now log in to our site. click to login http://127.0.0.1:8000/accounts/login/'.format(user.username)
    from_email = 'tuwaiq_community@outlook.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    return redirect('accounts:signup_requests')

def reject_signup(request, user_id):
    #retrieve the user with the ID and delete 
    user = get_object_or_404(User, id=user_id)
    user.delete()

    return redirect('accounts:signup_requests')

  

def bootCampsCategories(request :HttpRequest):
    return render(request,"accounts/bootCampsCategories.html" )


def waiting_list(request : HttpRequest):
     return render(request,"accounts/waiting_list.html")



#No permission page
def no_permission(request:HttpRequest):
    return render('accounts/no_permission.html')