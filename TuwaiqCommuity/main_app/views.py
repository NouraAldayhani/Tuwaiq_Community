from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Bootcamp, ContactUs
from django.contrib.auth.decorators import login_required

# Create your views here.

def welcome_page(request:HttpRequest):
    return render(request,'main_app/welcome.html')

@login_required
def about_page(request:HttpRequest):
    return render(request,'main_app/about.html')
 
def home_page(request:HttpRequest):   
    return render(request,'main_app/home.html')

@login_required
def bootcamps_page(request:HttpRequest):
    #check
    if not (request.user.is_staff and request.user.has_perm("main_app.view_bootcamp")):
        return redirect("accounts:no_permission_page")
    #view
    bootcamps = Bootcamp.objects.all()
    return render(request,'main_app/bootcamps.html', {'bootcamps':bootcamps})

@login_required
def create_bootcamp(request:HttpRequest):
    #check
    if not (request.user.is_staff and request.user.has_perm("main_app.add_bootcamp")):
        return redirect("accounts:no_permission_page")
    #add
    if request.method == 'POST':
        bootcamp_name = request.POST['name']
        bootcamp_category = request.POST['category']
        descripton = request.POST['bootcamp_descripton']
        bootcamp_start_date = request.POST['start_date']
        bootcamp_end_date = request.POST['end_date']
        new_bootcamp = Bootcamp(name=bootcamp_name, bootcamp_descripton=descripton, category=bootcamp_category, start_date=bootcamp_start_date, end_date=bootcamp_end_date)
        if "logo" in request.FILES:
            new_bootcamp.logo = request.FILES['logo']
        new_bootcamp.save()
        return redirect('main_app:bootcamps') 
    else:
        return render(request, "main_app/create_bootcamp.html", {'category_choices': Bootcamp.CATEGORY_CHOICES})

@login_required
def project_details(request:HttpRequest):
    return render(request, "main_app/project_details.html")

def my_bootcamp_page(request:HttpRequest):
    return render(request, "main_app/my_bootcamp.html")

@login_required
def add_contact(request:HttpRequest):
    #check
    if not (request.user.is_staff and request.user.has_perm("main_app.add_contactus")):
        return redirect("accounts:no_permission_page")
    #add
    context = None
    if request.method == 'POST':
        subject = request.POST['subject']
        descripton = request.POST['descripton']
        created_at = request.POST['created_at']
        new_contact = ContactUs(subject=subject, descripton=descripton, created_at=created_at)
        new_contact.save()
        context = "message sent successfully"
    return render(request, 'main_app/contact.html', {"msg":context})

@login_required
def delete_bootcamp(request:HttpRequest, bootcamp_id):
    #check
    if not (request.user.is_staff and request.user.has_perm("main_app.delete_bootcamp")):
        return redirect("accounts:no_permission_page")
    #delete
    try:
        bootcamp = Bootcamp.objects.get(id=bootcamp_id)
        bootcamp.delete()
        return redirect("main_app:bootcamps")
    except Bootcamp.DoesNotExist:
        return redirect("accounts:no_permission_page")

@login_required
def update_bootcamp(request:HttpRequest, bootcamp_id):
    #check
    if not (request.user.is_staff and request.user.has_perm("main_app.change_bootcamp")):
        return redirect("accounts:no_permission_page")
    #update
    bootcamp = Bootcamp.objects.get(id=bootcamp_id)
    if request.method == "POST":
        bootcamp.name = request.POST['name']
        bootcamp.bootcamp_descripton = request.POST["bootcamp_descripton"]
        bootcamp.category = request.POST["category"]
        bootcamp.start_date = request.POST["start_date"]
        bootcamp.end_date = request.POST["end_date"]
        if "logo" in request.FILES:
            bootcamp.logo = request.FILES['logo']
        bootcamp.save()
        return redirect("main_app:bootcamps")
    else:
        return render(request, 'main_app/update_bootcamp.html', {"bootcamp":bootcamp, 'category_choices':Bootcamp.CATEGORY_CHOICES})
