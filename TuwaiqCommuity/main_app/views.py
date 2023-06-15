from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from .models import Bootcamp

# Create your views here.
 
def home_page(request:HttpRequest):
    return render(request,'main_app/home.html')

def bootcamps_page(request:HttpRequest):
    bootcamps = Bootcamp.objects.all()
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