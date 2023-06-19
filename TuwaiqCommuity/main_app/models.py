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

    def __str__(self):
        return self.name

      
    
class Event(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bootcamp = models.ForeignKey(Bootcamp,on_delete=models.CASCADE)
    event_title = models.CharField(max_length=2000)
    event_descripton=models.TextField(blank=True)
    event_datetime = models.DateTimeField()
    event_location = models.URLField()
    event_image = models.ImageField(upload_to="images/",default="images/bootstrap.png")

    
class Attendance(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)



class Question(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    bootcamp = models.ForeignKey(Bootcamp, on_delete=models.CASCADE)
    subject=models.CharField(max_length=2000)
    question_description=models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    reply_description=models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    


class ContactUs(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length = 500, default = "Issue")
    created_at = models.DateTimeField(auto_now_add=True)
    descripton = models.TextField(blank = True)
   

    


