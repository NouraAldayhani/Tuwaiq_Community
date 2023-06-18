from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Bootcamp(models.Model):
    CATEGORY_CHOICES = [
           ("frontend", "Front-end Development"),
           ("frontend", "Back-end Development"),
           ("full_stack", "Full-stack Development"),
           ("UI", "UI/UX"),
           ("artificial", "Artificial Intelligence"),
           ("security", "Cyber Security"),         
    ]
    name=models.CharField(max_length=2000)
    bootcamp_descripton=models.TextField(blank=True)
    category=models.CharField(max_length=2000,choices=CATEGORY_CHOICES,default="Front-end Development")
    is_active=models.BooleanField(default=False)
    start_date=models.DateField(default=timezone.now)
    end_date=models.DateField(default=timezone.now() + timezone.timedelta(days=30))
    logo=models.ImageField(upload_to="images/",default="images/bootstrap.png")

    def members(self):
        return self.profile_set.all()

    def __str__(self):
        return self.name
      
class ContactUs(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length = 500, default = "issue")
    descripton = models.TextField(blank = True)




    

