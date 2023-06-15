from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from .models import Bootcamp

# Create your views here.

def profile(request:HttpRequest):
    return render(request,'accounts/profile.html')
