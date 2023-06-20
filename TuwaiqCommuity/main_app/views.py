from datetime import datetime
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
 

 #display upcoming events in the home page

@login_required
def home_page(request:HttpRequest):   
    upcoming_events = Event.objects.filter(event_datetime__gte=datetime.now())
    return render(request, 'main_app/home.html', {'upcoming_events': upcoming_events})


#____________________Bootcamp Section_________________________
@login_required
def bootcamps_page(request:HttpRequest):
    bootcamps = Bootcamp.objects.all()
    return render(request,'main_app/explore_bootcamps.html', {'bootcamps':bootcamps})



def bootcamp_page(request:HttpRequest, bootcamp_id):
    #try:
        bootcamp=Bootcamp.objects.get(id=bootcamp_id)
        members=bootcamp.profile_set.all()
        members_count= bootcamp.get_member_count()
        questions = Question.objects.filter(bootcamp=bootcamp).order_by('timestamp')
        return render(request, "main_app/bootcamp.html",{"bootcamp":bootcamp,"members": members,'questions': questions,"members_count": members_count }) 


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



def is_active_bootcamp(request:HttpRequest,bootcamp_id):
    try:
        if request.method == "POST":
            bootcamp=Bootcamp.objects.get(id=bootcamp_id)
            if bootcamp.is_active:
                bootcamp.is_active=False
            else:
                bootcamp.is_active=True
            
            bootcamp.save()
    except:
        #show not found page
        return render(request, 'main_app/not_found.html')
    
    return redirect(request.GET.get("next", "/"))



#_____________________________________________
@login_required
def project_details(request:HttpRequest):
    return render(request, "main_app/project_details.html")
 
#____________________Questin Section_________________________
def add_question(request:HttpRequest, bootcamp_id):
    if request.method == 'POST':
            bootcamp = Bootcamp.objects.get(id=bootcamp_id)
            subject = request.POST.get('subject')
            question_description=request.POST.get('question_description')
            question = Question.objects.create(subject=subject, bootcamp=bootcamp, question_description=question_description, user = request.user)
            question.save()
    return redirect('main_app:bootcamp_page', bootcamp_id=bootcamp_id)


def update_question(request:HttpRequest, bootcamp_id):
    pass



def delete_question(request:HttpRequest, bootcamp_id):
    pass

#____________________Reply Section_________________________
def reply_detail(request:HttpRequest,question_id):
    question = Question.objects.get(id=question_id)
    replies = Reply.objects.filter(question=question)   
    return render(request, "main_app/reply_detail.html",{'question': question, 'replies': replies})


def update_reply(request:HttpRequest, question_id):
    pass


def delete_reply(request:HttpRequest, question_id):
    pass


def add_reply(request:HttpRequest,question_id):
    question = Question.objects.get(id=question_id)
    bootcamp = question.bootcamp
    members = bootcamp.get_members()
    for member in members:
        print(member)
    if request.user in members:
        if request.method == 'POST':
            reply_description = request.POST.get('reply_description')
            reply = Reply.objects.create(user=request.user,question=question,reply_description=reply_description)
            reply.save()
            return redirect('main_app:reply_detail', question_id=question.id)
        
        return render(request, 'main_app/reply_detail.html', {'question': question, "members": members })
    else:
        return HttpResponse("You are not a member of this bootcamp.")



#____________________Event Section_________________________
#events based on the category
def events(request):
    #retrieve full-stack category events
    fullstack_bootcamps = Bootcamp.objects.filter(category='full_stack')
    fullstack_events = Event.objects.filter(bootcamp__in=fullstack_bootcamps)
    #retrieve front-end category events
    frontend_bootcamps = Bootcamp.objects.filter(category='frontend')
    frontend_events = Event.objects.filter(bootcamp__in=frontend_bootcamps)
    #retrieve back-end category events
    backend_bootcamps = Bootcamp.objects.filter(category='backend')
    backend_events = Event.objects.filter(bootcamp__in=backend_bootcamps)
    #retrieve UI/UX category events
    UIUX_bootcamps = Bootcamp.objects.filter(category='UI')
    UIUX_events = Event.objects.filter(bootcamp__in=UIUX_bootcamps)
    #retrieve AI category events
    artificial_bootcamps = Bootcamp.objects.filter(category='artificial')
    artificial_events = Event.objects.filter(bootcamp__in=artificial_bootcamps)
    #retrieve Cyper security category events
    security_bootcamps = Bootcamp.objects.filter(category='security')
    security_events = Event.objects.filter(bootcamp__in=security_bootcamps)

    context = {
        'frontend_events': frontend_events,
        'fullstack_events': fullstack_events,
        'backend_events': backend_events,
        'UIUX_events': UIUX_events,
        'artificial_events': artificial_events,
        'security_events': security_events,
    }
    return render(request, 'main_app/events.html', context)



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
        user_attending_event = False
        if request.user.is_authenticated:
            user_attendance = Attendance.objects.filter(event=event, user=request.user).first()
            if user_attendance:
                user_attending_event = True
        if request.method == 'POST' and 'attend_button' in request.POST:
            user = request.user
            if request.POST['attend_button'] == 'Attend':
                attendance = Attendance.objects.filter(event=event, user=user).first()
                if attendance:
                    messages.error(request, 'You have already attended this event.')
                else:
                    attendance = Attendance(event=event, user=user)
                    attendance.save()
                    messages.success(request, 'You have successfully attended the event.')
            elif request.POST['attend_button'] == 'Unattend':
                attendance = Attendance.objects.filter(event=event, user=user).first()
                if attendance:
                    attendance.delete()
                    messages.success(request, 'You have successfully unattended the event.')
                else:
                    messages.error(request, 'You are not attending this event.')
            return redirect('main_app:event_details', event_id=event.id)

        context = {'event': event, 'attendees': attendees, 'user_attending_event': user_attending_event}
        return render(request, 'main_app/event_details.html', context)
    except Event.DoesNotExist:
        messages.error(request, 'The event you are looking for does not exist.')
        return redirect("main_app:bootcamp_event",bootcamp_id=bootcamp_id)


@login_required
def update_event(request:HttpRequest,event_id):  
    event = Event.objects.get(id=event_id)


    if request.method == "POST":
        event.event_title = request.POST["event_title"]
        event.event_descripton = request.POST["event_descripton"]
        event.event_datetime = request.POST["event_datetime"]
        event.event_location = request.POST["event_location"]
        if "image" in request.FILES:
            event.event_image = request.FILES["event_image"]
        event.save()
        messages.success(request, 'Event updated successfully.')
        return redirect("main_app:event_details", event_id=event.id)
    return render(request, 'main_app/update_event.html', {'event':event})

    
    
@login_required()
def delete_event(request:HttpRequest, event_id):   
    event = Event.objects.get(id=event_id)
    bootcamp_id = event.bootcamp.id
    event.delete()
    return redirect("main_app:bootcamp_event",bootcamp_id=bootcamp_id)




 #____________________Contact Section_________________________
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



#____________________Notification Section_________________________
def notifications(request):
    return render(request, 'main_app/notification.html')
  
 