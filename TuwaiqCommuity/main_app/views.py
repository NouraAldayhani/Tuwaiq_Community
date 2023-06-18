from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Bootcamp, ContactUs

# Create your views here.

def welcome_page(request:HttpRequest):
    return render(request,'main_app/welcome.html')

def about_page(request:HttpRequest):
    return render(request,'main_app/about.html')
 
def home_page(request:HttpRequest):   
    return render(request,'main_app/home.html')



def bootcamps_page(request:HttpRequest, booobtcamp_id):
    bootcamps = Bootcamp.objects.get(id=)
    return render(request,'main_app/bootcamps.html', {'bootcamps':bootcamps})


def create_bootcamp(request:HttpRequest):
    #check if the user is the manager
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
        return render(request,'main_app/create_bootcamp.html')
    


def project_details(request:HttpRequest):
    return render(request, "main_app/project_details.html")



def my_bootcamp_page(request:HttpRequest):
    
    return render(request, "main_app/my_bootcamp.html")



def add_contact(request:HttpRequest):
    context = None
    if request.method == 'POST':
        subject = request.POST['subject']
        descripton = request.POST['descripton']
        created_at = request.POST['created_at']
        new_contact = ContactUs(subject=subject, descripton=descripton, created_at=created_at)
        new_contact.save()
        context = "message sent successfully"
    return render(request, 'main_app/contact.html', {"msg":context})
