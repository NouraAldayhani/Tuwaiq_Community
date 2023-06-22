from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Bootcamp, ContactUs,Question,Reply,Event, Attendance, Notification
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.


def welcome_page(request:HttpRequest):
    return render(request,'main_app/welcome.html')

def about_page(request:HttpRequest):
    return render(request,'main_app/about.html')
 

 #display upcoming events in the home page

@login_required
def home_page(request:HttpRequest):
    if request.user.is_staff:
        #if user staff, get only the upcoming events
        upcoming_events = Event.objects.filter(event_datetime__gte=datetime.now())
        return render(request, 'main_app/home.html', {'upcoming_events': upcoming_events})
    else:
        try:
            #if user is not staff, get their profile and bootcamp
            user_profile = Profile.objects.get(user=request.user)
            user_bootcamp = user_profile.bootcamp
            upcoming_events = Event.objects.filter(event_datetime__gte=datetime.now())

            # Render the home page with the user's bootcamp and upcoming events
            return render(request, 'main_app/home.html', {'upcoming_events': upcoming_events, 'user_bootcamp':user_bootcamp})
        except Profile.DoesNotExist:
            #if the user does not have a profile
            messages.error(request, 'You do not have a profile.')
            return redirect('accounts:sign_up')


#____________________Bootcamp Section_________________________
@login_required
def bootcamps_page(request:HttpRequest):
    bootcamps = Bootcamp.objects.all()
    return render(request,'main_app/explore_bootcamps.html', {'bootcamps':bootcamps})


@login_required
def bootcamp_page(request, bootcamp_id):

    try:
        bootcamp=Bootcamp.objects.get(id=bootcamp_id)
        members=bootcamp.get_members()
        members_count= bootcamp.get_member_count()
        questions = Question.objects.filter(bootcamp=bootcamp).order_by('timestamp')
        update_question = None
    except:
        messages.error(request, 'An error occurred while retrieving the bootcamp.',extra_tags='msg-deleted')
        return redirect('main_app:home_page')

    if request.method == 'POST':
        if 'add_question' in request.POST:
            subject = request.POST.get('subject')
            question_description = request.POST.get('question_description')
            user = request.user
            Question.objects.create(subject=subject, question_description=question_description, user=user, bootcamp=bootcamp)
            return redirect('main_app:bootcamp_page', bootcamp_id=bootcamp_id)
        else:
            question_id = request.POST.get('question_id')
            question = Question.objects.get(id=question_id, bootcamp=bootcamp)
            update_question = question

    return render(request, 'main_app/bootcamp.html', {'bootcamp': bootcamp, 'questions': questions, 'update_question': update_question,"members": members,"members_count": members_count})



@login_required
def create_bootcamp(request:HttpRequest):
    #check if the user is the manager
    #add
    if not (request.user.is_staff and request.user.has_perm("main_app.add_bootcamp")):
        return redirect("accounts:no_permission")
    if request.method == 'POST':
        try:
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
        except Exception:
            context = "please try again"
            return render(request,'main_app/create_bootcamp.html', {"msg":context, "category_choices":Bootcamp.CATEGORY_CHOICES})
    else:
        return render(request,'main_app/create_bootcamp.html', {"category_choices":Bootcamp.CATEGORY_CHOICES})



@login_required
def update_bootcamp(request:HttpRequest, bootcamp_id):
    if not (request.user.is_staff and request.user.has_perm("main_app.change_bootcamp")):
        return redirect("accounts:no_permission")
    bootcamp = Bootcamp.objects.get(id=bootcamp_id)
    #update
    if request.method == "POST":
        try:
            bootcamp.name = request.POST["name"]
            bootcamp.category = request.POST["category"]
            bootcamp.bootcamp_descripton = request.POST["bootcamp_descripton"]
            bootcamp.start_date = request.POST["start_date"]
            bootcamp.end_date = request.POST["end_date"]
            if "logo" in request.FILES:
                bootcamp.logo = request.FILES["logo"]
            bootcamp.save()
            messages.success(request, 'Bootcamp updated successfully')
            return redirect("main_app:bootcamps")
        except Exception:
            context = "please try again"
            return render(request,'main_app/update_bootcamp.html', {"msg":context, "category_choices":Bootcamp.CATEGORY_CHOICES})
    return render(request, 'main_app/update_bootcamp.html', {"bootcamp":bootcamp, "category_choices":Bootcamp.CATEGORY_CHOICES})




@login_required
def delete_bootcamp(request:HttpRequest, bootcamp_id):
    #check
    if not (request.user.is_staff and request.user.has_perm("main_app.delete_bootcamp")):
        return redirect("accounts:no_permission")
    #delete
    bootcamp = Bootcamp.objects.get(id = bootcamp_id)
    bootcamp.delete()
    messages.success(request, 'Bootcamp deleted successfully')
    return redirect("main_app:bootcamps")



@login_required
def is_active_bootcamp(request:HttpRequest,bootcamp_id):
    try:     
        bootcamp=Bootcamp.objects.get(id=bootcamp_id)
        if bootcamp.is_active:
            bootcamp.is_active=False
        else:
            bootcamp.is_active=True        
        bootcamp.save()
    except:
        return render(request, 'main_app/not_found.html')   
    return redirect(request.GET.get("next", "/"))



 
#____________________Question Section_________________________
@login_required
def add_question(request:HttpRequest, bootcamp_id):
    if request.method == 'POST':
            bootcamp = Bootcamp.objects.get(id=bootcamp_id)
            subject = request.POST.get('subject')
            question_description=request.POST.get('question_description')
            question = Question.objects.create(subject=subject, bootcamp=bootcamp, question_description=question_description, user = request.user)
            question.save()
    return redirect('main_app:bootcamp_page', bootcamp_id=bootcamp_id)


@login_required
def update_question(request: HttpRequest, bootcamp_id, question_id=None):
    bootcamp = Bootcamp.objects.get(id=bootcamp_id)
    members=bootcamp.get_members()
    # If the request method is POST, we process the form data
    if request.method == 'POST':
        # Extract the form data from the request
        subject = request.POST.get('subject')
        question_description = request.POST.get('question_description')
        user = request.user

        # If the subject field is empty, display an error message and redirect back to the bootcamp page
        if not subject:
            messages.error(request, 'Subject is required.', extra_tags='msg-deleted')
            return redirect('main_app:bootcamp_page', bootcamp_id=bootcamp_id)

        # If the question_id parameter is present, we update the existing question
        if question_id:
            question = Question.objects.get(id=question_id, bootcamp=bootcamp)
            question.subject = subject
            question.question_description = question_description
            question.user = user
            question.save()  # save the changes to the question object
        # If the question_id parameter is not present, we create a new question
            messages.success(request, 'Your question updated successfully.', extra_tags='msg-deleted')
        else:
            question = Question.objects.create(subject=subject, question_description=question_description, user=user, bootcamp=bootcamp)
        # Create notifications for all members of the bootcamp group
            for member in members:
                if member != user:
                    notification = Notification(user=member, content=f"New question from {user.first_name}")
                    notification.save()
        # Save the question to the database and redirect to the bootcamp page
        return redirect('main_app:bootcamp_page', bootcamp_id=bootcamp_id)

    # If the request method is not POST, we retrieve the question (if specified) and the list of questions for the bootcamp
    update_question = None
    if question_id:
        update_question = Question.objects.get(id=question_id, bootcamp=bootcamp)

    questions = Question.objects.filter(bootcamp=bootcamp)

    # Pass the bootcamp, questions, and update_question variables to the template
    return render(request, 'main_app/bootcamp.html', {'bootcamp': bootcamp, 'questions': questions, 'update_question': update_question})




@login_required
def delete_question(request, bootcamp_id, question_id):
    bootcamp = Bootcamp.objects.get(id=bootcamp_id)
    question = Question.objects.get(id=question_id, bootcamp=bootcamp)  
    # Only the user who created the question or a manager can delete it
    if request.user == question.user or request.user.is_staff:
        try:
            question.delete()
            messages.success(request, 'Question deleted successfully.', extra_tags='reply-deleted')
        except:
            messages.error(request, 'An error occurred while deleting all questions.',extra_tags='msg-deleted')
    else:
        return redirect('accounts:no_permission')
    
    return redirect('main_app:bootcamp_page', bootcamp_id=bootcamp_id)




@login_required
def delete_all_questions(request, bootcamp_id):
    # Only managers can delete all questions
    if not request.user.has_perm("main_app.delete_question"):
        return redirect('accounts:no_permission')   
    # Delete all questions in the bootcamp
    try:
        Question.objects.filter(bootcamp_id=bootcamp_id).delete()
        messages.success(request, 'All questions deleted successfully.', extra_tags='msg-deleted')
    except:
        messages.error(request, 'An error occurred while deleting question.',extra_tags='msg-deleted')
    return redirect('main_app:bootcamp_page', bootcamp_id=bootcamp_id)




#____________________Reply Section_________________________

@login_required
def reply_detail(request:HttpRequest,question_id):
    try:
        question = Question.objects.get(id=question_id)
        members=question.bootcamp.get_members()
        replies = Reply.objects.filter(question=question)
    except:
        messages.error(request, 'An error occurred while retrieving the question and replies.',extra_tags='msg-deleted')
        return redirect('main_app:home_page')   
    return render(request, "main_app/reply_detail.html",{'question': question, 'replies': replies,'members':members})



@login_required
def update_reply(request:HttpRequest, reply_id):
    try:
        reply = Reply.objects.get(id=reply_id)
        question = reply.question
        bootcamp = question.bootcamp
        members = bootcamp.get_members()
    except:
        messages.error(request, 'An error occurred while retrieving the reply.',extra_tags='msg-deleted')
        return redirect('main_app:home_page')
    if request.user in members:
        if request.method == 'POST':
            try:
                reply_description = request.POST.get('reply_description')
                reply.reply_description = reply_description
                if request.user == reply.user or  request.user.has_perm("main_app.delete_reply"):
                    reply.save()
                    messages.success(request, 'Reply updated successfully.', extra_tags='msg-deleted')
                else:
                    return redirect("accounts:no_permission_page")
            except:
                messages.error(request, 'An error occurred while updating the reply.', extra_tags='msg-deleted')
                return redirect('main_app:home_page')
            return redirect('main_app:reply_detail', question_id=question.id)

        return render(request, 'main_app/update_reply.html', {'reply': reply, 'question': question, 'members': members,'bootcamp': bootcamp })
    else:
        messages.error(request, 'You are not a member of this bootcamp.')
        return redirect('main_app:home_page')



@login_required
def delete_reply(request:HttpRequest, reply_id):
    try:
        reply = Reply.objects.get(id=reply_id)
        question = reply.question
    except:
        messages.error(request, 'An error occurred while retrieving the reply.', extra_tags='msg-deleted')
        return redirect('main_app:home_page')
    try:
        if request.user == reply.user or  request.user.has_perm("main_app.delete_reply"):
            reply.delete()
            messages.success(request, 'Reply deleted successfully.', extra_tags='msg-deleted')
        else:
            return redirect("accounts:no_permission_page")
    except:
        messages.error(request, 'An error occurred while deleting the reply.', extra_tags='msg-deleted')
        return redirect('main_app:home_page')
    return redirect('main_app:reply_detail', question_id=question.id)




@login_required
def add_reply(request:HttpRequest,question_id):
    try:
        question = Question.objects.get(id=question_id)
        bootcamp = question.bootcamp
        members = bootcamp.get_members()
    except Question.DoesNotExist:
        messages.error(request, "Invalid question ID.", extra_tags='msg-deleted')
        return redirect('main_app:home_page')
    except Bootcamp.DoesNotExist:
        messages.error(request, "Question does not belong to a valid bootcamp.", extra_tags='msg-deleted')
        return redirect('main_app:home_page')   
    
    if  request.user.has_perm("main_app.add_reply") or request.user in members:
        if request.method == 'POST':
            reply_description = request.POST.get('reply_description')
            try:
                reply = Reply.objects.create(user=request.user,question=question,reply_description=reply_description)
                reply.save()
                messages.success(request, 'Reply added successfully.', extra_tags='msg-deleted')
            except:
                messages.error(request, "An error occurred while creating the reply.", extra_tags='msg-deleted')
            
            return redirect('main_app:reply_detail', question_id=question.id)
        
        return render(request, 'main_app/reply_detail.html', {'question': question, "members": members })
    else:
        messages.error(request, "You are not a member of this bootcamp.", extra_tags='msg-deleted')
        return redirect('main_app:home_page')



#____________________Event Section_________________________
#events based on the category
@login_required
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
@login_required
def bootcamp_event(request:HttpRequest,bootcamp_id):
    try:
        bootcamp = Bootcamp.objects.get(id = bootcamp_id)
        # Check for and delete past events
        past_events = Event.objects.filter(bootcamp=bootcamp, event_datetime__lt=datetime.now())
        past_events.delete()
        events = Event.objects.filter(bootcamp=bootcamp)
        return render(request, "main_app/bootcamp_event.html", {'bootcamp': bootcamp, 'events': events})
    except Bootcamp.DoesNotExist:
        messages.error(request, 'The bootcamp you are trying to view does not exist.')
        return redirect('main_app:home_page')
  
  
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

  
@login_required
def event_details(request:HttpRequest,event_id):
    bootcamp_id = None
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
                    messages.error(request, 'You have already attended this event.', extra_tags='msg-deleted')
                else:
                    attendance = Attendance(event=event, user=user)
                    attendance.save()
                    notification = Notification(user=user, content=f"{user.first_name}  will attend {event.event_title}")
                    notification.save()

                    messages.success(request, 'You have successfully added to attendees list.')

   
            elif request.POST['attend_button'] == 'Unattend':
                attendance = Attendance.objects.filter(event=event, user=user).first()
                if attendance:
                    attendance.delete()
                    notification = Notification(user=user, content=f" {user.first_name} will not attend to {event.event_title}")
                    notification.save()

                    messages.success(request, 'You have successfully removed from attendees list.')

                else:
                    messages.error(request, 'You are not attending this event.', extra_tags='msg-deleted')
            return redirect('main_app:event_details', event_id=event.id)

        context = {'event': event, 'attendees': attendees, 'user_attending_event': user_attending_event}
        return render(request, 'main_app/event_details.html', context)
    except Event.DoesNotExist:

        messages.error(request, 'The event you are looking for does not exist.',extra_tags='msg-deleted')
        if bootcamp_id:
            return redirect('main_app:bootcamp_event', bootcamp_id=bootcamp_id)
        else:
            return redirect('main_app:home_page')





@login_required
def update_event(request:HttpRequest,event_id): 
    try: 
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
    except Event.DoesNotExist:
        messages.error(request, 'The event you are trying to update does not exist.',extra_tags='msg-deleted')
        return redirect('main_app:home_page')

      

    
    
@login_required()
def delete_event(request:HttpRequest, event_id):
    try:   
        event = Event.objects.get(id=event_id)
        bootcamp_id = event.bootcamp.id
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect("main_app:bootcamp_event",bootcamp_id=bootcamp_id)
    except Event.DoesNotExist:
        messages.error(request, 'The event you are trying to delete does not exist.',extra_tags='msg-deleted')
        return redirect('main_app:home_page')


  
  

 #____________________Contact Section_________________________

@login_required
def add_contact(request:HttpRequest):
    context = None
    if request.method == 'POST':
        subject = request.POST['subject']
        descripton = request.POST['descripton']
        created_at = request.POST['created_at']
        new_contact = ContactUs(user=request.user, subject=subject, descripton=descripton, created_at=created_at)
        new_contact.save()
        context = "message sent successfully"
    return render(request, 'main_app/contact.html', {"msg":context})


#____________________Notification Section_________________________
@login_required
def notification_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-id")
    return render(request, 'main_app/notification.html', {'notifications': notifications})



@csrf_exempt
def delete_notification(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification does not exist'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

#____________________Search page___________________________________

def search_page(request:HttpRequest):
    search_phrase = request.GET.get("search", "")
    bootcamps = Bootcamp.objects.filter(name__contains=search_phrase, category__contains=search_phrase)

    return render(request, "main_app/search_page.html", {"bootcamps" : bootcamps})
