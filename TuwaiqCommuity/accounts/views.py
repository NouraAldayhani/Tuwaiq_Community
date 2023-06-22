from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Bootcamp,Profile,Project
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
                messages.error(request, 'Please select a bootcamp.', extra_tags='msg-deleted')
                return redirect('accounts:sign_up')
        except:
                 messages.error(request, 'Please choose another username!', extra_tags='msg-deleted')
                 return redirect('accounts:sign_up')
        # Validate form data
        if not bootcamp_name:
            messages.error(request, 'Please select a bootcamp.', extra_tags='msg-deleted')
            return redirect('accounts:sign_up')

        # Retrieve Bootcamp object from database
        bootcamp_qs = Bootcamp.objects.filter(name=bootcamp_name)
        if not bootcamp_qs.exists():
            messages.error(request, f'Bootcamp "{bootcamp_name}" does not exist.', extra_tags='msg-deleted')
            return redirect('accounts:sign_up')
        bootcamp = bootcamp_qs.first()

        # Create User object
        user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name,is_active=False)

        # Create Profile object
        profile = Profile(user=user, bootcamp=bootcamp)
        profile.save()
        messages.success(request, f'Your account request has been submitted for approval. Please wait for confirmation.', extra_tags='msg-deleted')
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
            msg = "Incorrect Credentials or your request has not been approved yet"
      
    return render(request, "accounts/login.html", {"msg" : msg })




def log_out(request: HttpRequest):
    logout(request)
    return redirect("main_app:welcome_page")




@login_required
def profile(request:HttpRequest, user_id):
    '''if request.user.profile.id != profile_id:
        return redirect("accounts:no_permission")'''
    user=User.objects.get(id=user_id)
    try:
        profile = Profile.objects.get(user=user)
        projects = Project.objects.filter(profile=profile)
    except:
        return render(request, "main_app/not_found.html")
    return render(request, "accounts/profile.html", {"profile":profile, "projects":projects})




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
    if (request.user.is_staff):
        #retrive inactive users and their bootcamp name
        inactive_users = User.objects.filter(is_active=False, is_staff=False).select_related('profile__bootcamp')
        num_requests = inactive_users.count()
    else:
        return redirect('accounts:no_permission')
    
    return render(request, "accounts/signup_requests.html", {"inactive_users":inactive_users, "num_requests":num_requests})



def approve_signup(request, user_id):
    #retrieve the user with the ID and activate user account
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, 'User activated successfully')
    #Send email activate notification to user
    subject = 'Your account has been activated'
    message = 'Dear {}, your account has been activated. You can now log in to our site. click to login http://127.0.0.1:8000/accounts/login/'.format(user.username)
    from_email = 'tuwaiq_community@outlook.com'
    recipient_list = [user.email]
    try:
        send_mail(subject, message, from_email, recipient_list)
    except:
        messages.success(request, 'email sent successfully')
        return redirect('accounts:signup_requests')
                 
    return redirect('accounts:signup_requests')



def reject_signup(request, user_id):
    #retrieve the user with the ID and delete 
    try:
        user = get_object_or_404(User, id=user_id)
        user.delete()
        #Send email activate notification to user
        subject = 'Your account has been activated'
        message = 'Dear {}, your sign up request have been rejected please make sure your entred a valid information. If you want to send new request click to sign-up http://127.0.0.1:8000/accounts/signup/'.format(user.username)
        from_email = 'tuwaiq_community@outlook.com'
        recipient_list = [user.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
        except:
            messages.success(request, 'email sent successfully')
            return redirect('accounts:signup_requests')
        messages.success(request, 'User rejected successfully') 
    except User.DoesNotExist:
        messages.error(request, 'User not found')
    except Exception:
        messages.error(request, 'An error occurred while processing your request')
    return redirect('accounts:signup_requests')
    
   


def bootCampsCategories(request :HttpRequest):
    return render(request,"accounts/bootCampsCategories.html" )



def waiting_list(request : HttpRequest):
     return render(request,"accounts/waiting_list.html")



#No permission page
def no_permission(request:HttpRequest):
    return render(request, 'accounts/no_permission.html')




@login_required
def add_project(request: HttpRequest, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    context = {}
    if not (request.user.is_authenticated and request.user.profile.id == int(user.profile.id)):
        return redirect("accounts:no_permission")
    if request.method == 'POST':
        try:
            project_title = request.POST['project_title']
            project_date = request.POST['project_date']
            project_description = request.POST['project_description']
            type_project = request.POST['type_project']
            github_link = request.POST.get('github_link', '') # set default value to empty string
            powerpoint_file = request.FILES.get('powerpoint_file', None) # set default value to None
            project_document = request.FILES.get('project_document', None) # set default value to None
            project_logo = request.FILES.get('project_logo', 'images/default_avatar.png') # set default value to default avatar image path
            new_project = Project(profile=profile, project_title=project_title, project_date=project_date, project_description=project_description, type_project=type_project, github_link=github_link, powerpoint_file=powerpoint_file, project_document=project_document, project_logo=project_logo)
            new_project.save()
            return redirect('accounts:profile', user_id=request.user.id) 
        except Exception:
            context['msg'] = "Please try again."
            context['type_choices'] = Project.TYPE_CHOICES
            return render(request, 'accounts/add_project.html', {"user": user, **context})
    context['type_choices'] = Project.TYPE_CHOICES
    return render(request, 'accounts/add_project.html', {"user": user, **context})


@login_required
def project_details(request:HttpRequest, project_id):
    project = Project.objects.get(id=project_id)
    return render(request, "accounts/project_details.html", {'project':project})


@login_required
def delete_project(request:HttpRequest, project_id):
    project = Project.objects.get(id = project_id)
    #check
    if not (request.user.is_authenticated and request.user.id == int(project.profile.user.id)):
        return redirect("accounts:no_permission")
    #delete
    project.delete()
    messages.success(request, 'Project deleted successfully')
    return redirect("accounts:profile", user_id=request.user.id)


def update_project(request:HttpRequest, project_id):
    project = Project.objects.get(id=project_id)
    #check
    if not (request.user.is_authenticated and request.user.id == int(project.profile.user.id)):
        return redirect("accounts:no_permission")
    #update
    if request.method == "POST":
        try:
            try:
                project.project_title = request.POST["project_title"]
                project.project_date = request.POST['project_date']
                project.project_description = request.POST['project_description']
                project.type_project = request.POST['type_project']
            except:
                context = "You must fill the required fields"
                return render(request,'accounts/update_project.html', {'msg':context, 'type_choices':Project.TYPE_CHOICES})
            if "powerpoint_file" in request.FILES:
                project.powerpoint_file = request.FILES['powerpoint_file']

            if "github_link" in request.FILES:
                project.github_link = request.POST['github_link']
          
            if "project_document" in request.FILES:
                project.project_document = request.FILES['project_document']

            if "project_logo" in request.FILES:
                project.project_logo = request.FILES["project_logo"]

            project.save()
            return redirect("accounts:project_details", project_id=project_id)
        except Exception:
            context = "please try again"
            return render(request,'accounts/update_project.html', {'msg':context, 'type_choices':Project.TYPE_CHOICES})
    return render(request, 'accounts/update_project.html', {'project':project, 'type_choices':Project.TYPE_CHOICES})

 

