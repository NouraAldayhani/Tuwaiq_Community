from django.db import models
from django.contrib.auth.models import User
from main_app.models import Bootcamp

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bootcamp = models.ForeignKey(Bootcamp,on_delete=models.CASCADE)
    about_user = models.CharField(max_length=2048, blank=True)
    avatar = models.ImageField(upload_to="images/", default="images/bootstrap.png")
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)


    
