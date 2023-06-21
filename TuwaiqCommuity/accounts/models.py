from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from main_app.models import Bootcamp

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bootcamp = models.ForeignKey(Bootcamp,on_delete=models.CASCADE)
    about_user = models.CharField(max_length=2048, blank=True)
    avatar = models.ImageField(upload_to="images/", default="images/user_default.png")
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)


class Project(models.Model):
    TYPE_CHOICES = [
           ("unit", "Unit Project"),
           ("capstone", "Capstone Project"),              
    ]
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    project_title=models.CharField(max_length=2048)
    project_description=models.TextField()
    project_date=models.DateField(default=timezone.now)
    type_project=models.CharField(max_length=2000,choices=TYPE_CHOICES,default="Unit Project")
    project_logo = models.ImageField(upload_to="images/",default="images/default_avatar.png")
    github_link= models.URLField(blank=True)
    powerpoint_file= models.FileField(upload_to='documents/', blank=True)
    project_document=models.FileField(upload_to='documents/', blank=True)

