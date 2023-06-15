from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.

def request_page(request : HttpRequest):
    return render(request, "accounts/request.html")