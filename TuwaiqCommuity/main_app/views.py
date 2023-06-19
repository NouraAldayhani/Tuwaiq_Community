from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Bootcamp, ContactUs,Question,Reply,Event, Attendance
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


def welcome_page(request:HttpRequest):
    return render(request,'main_app/welcome.html')

def about_page(request:HttpRequest):
    return render(request,'main_app/about.html')
 
@login_required
def home_page(request:HttpRequest):   
    return render(request,'main_app/home.html')

@login_required
def bootcamps_page(request:HttpRequest):
    bootcamps = Bootcamp.objects.all()
    return render(request,'main_app/explore_bootcamps.html', {'bootcamps':bootcamps})

@login_required
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
        return redirect('main_app:bootcamps',) 
    else:
        return render(request,'main_app/create_bootcamp.html')

@login_required
def update_bootcamp(request:HttpRequest, bootcamp_id):
    #check if the user is the manager

    return render(request, "main_app/update_bootcamp.html")

@login_required
def delete_bootcamp(request:HttpRequest, bootcamp_id):
    #check
    if not (request.user.is_staff and request.user.has_perm("main_app.delete_bootcamp")):
        return redirect("accounts:no_permission")
    #delete
    bootcamp = Bootcamp.objects.get(id = bootcamp_id)
    bootcamp.delete()
    return redirect("main_app:bootcamps")

@login_required
def project_details(request:HttpRequest):
    return render(request, "main_app/project_details.html")


def bootcamp_page(request:HttpRequest, bootcamp_id):
    #try:
        bootcamp=Bootcamp.objects.get(id=bootcamp_id)
        members=bootcamp.profile_set.all()
        members_count= bootcamp.get_member_count()
        questions = Question.objects.filter(bootcamp=bootcamp)
        return render(request, "main_app/bootcamp.html",{"bootcamp":bootcamp,"members": members,'questions': questions,"members_count": members_count })    
   # except:
        #return render(request,"accounts/no_permission.html")


def add_question(request:HttpRequest, bootcamp_id):
    if request.method == 'POST':
            bootcamp = Bootcamp.objects.get(id=bootcamp_id)
            subject = request.POST.get('subject')
            question_description=request.POST.get('question_description')
            question = Question(subject=subject, bootcamp=bootcamp, user=request.user, question_description=question_description)
            question.save()
    return redirect('main_app:bootcamp_page', bootcamp_id=bootcamp_id)


def rply_detail(request:HttpRequest):
    return render(request, "main_app/reply_detail.html")




# user's bootcamp events views
def bootcamp_event(request:HttpRequest,bootcamp_id):
    bootcamp = Bootcamp.objects.get(id = bootcamp_id)
    events = Event.objects.filter(bootcamp=bootcamp)
    return render(request, "main_app/bootcamp_event.html", {'bootcamp': bootcamp, 'events': events})
  
  
  
@login_required
def create_event(request:HttpRequest,bootcamp_id):  
    bootcamp = Bootcamp.objects.get(id=bootcamp_id)
    if request.method == 'POST':
        try:
            new_event = Event(user=request.user, bootcamp=bootcamp, event_title=request.POST['event_title'], event_descripton=request.POST['event_descripton'], event_datetime=request.POST['event_datetime'], event_location=request.POST['event_location'])
            if "event_image" in request.FILES:
                new_event.event_image= request.FILES['event_image']
            new_event.save()
            return redirect('main_app:bootcamp_event', bootcamp_id=bootcamp_id) 
        except Exception as e:
                print(f"Error creating event: {e}")
                return redirect('main_app:bootcamp_event', bootcamp_id=bootcamp_id)
    else:
        return render(request, 'main_app/create_event.html', {'bootcamp': bootcamp})

  

def event_details(request:HttpRequest,event_id):
    try:
        event = Event.objects.get(id = event_id)
        bootcamp_id = event.bootcamp.id
        attendees = Attendance.objects.filter(event=event).select_related('user__profile__bootcamp')
        if request.method == 'POST' and 'attend_button' in request.POST:
            user = request.user
            attendance = Attendance.objects.filter(event=event, user=user).first()
            if attendance:
                messages.error(request, 'You have already attended this event.')
            else:
                attendance = Attendance(event=event, user=user)
                attendance.save()
                messages.success(request, 'You have successfully attended the event.')
            return redirect('main_app:event_details', event_id=event.id)
        
        return render(request, 'main_app/event_details.html', {'event': event, 'attendees': attendees})
    except Event.DoesNotExist:
        messages.error(request, 'The event you are looking for does not exist.')
        return redirect("main_app:bootcamp_event",bootcamp_id=bootcamp_id)
      
    
    
@login_required()
def delete_event(request:HttpRequest, event_id):   
    event = Event.objects.get(id=event_id)
    bootcamp_id = event.bootcamp.id
    event.delete()
    return redirect("main_app:bootcamp_event",bootcamp_id=bootcamp_id)
  
  
@login_required
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
