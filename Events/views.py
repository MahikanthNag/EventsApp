from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
# Create your views here.
from django.template.context import RequestContext
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Events.models import *
from Events.serializers import SnippetSerializer

# Create your views here.
from django.template import loader
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import logout
from httpie.models import HTTPResponse
from Events.forms import *
import datetime as dt
import time
# from Events.models import EventsList

def logout1(request):
    logout(request)
    return HttpResponseRedirect("/login/")


# def loginPage(request):


def get_registrationform(request):
    if(request.method=='POST'):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']

            # location=form.cleaned_data['location']
            password1=form.cleaned_data['password1']
            password2=form.cleaned_data['password2']
            ID=form.cleaned_data['ID']
            if password1==password2:
                # u=User.objects.create_superuser(username,email,password1)
                if len(ID)==4:
                    r=Faculty(name=username,staffid=ID,password=password1,emailid=email)
                    r.save()
                    return HttpResponseRedirect("/login")
                else:
                    r=Students(name=username,rollno=ID,password=password1)
                    r.save()
                    return HttpResponseRedirect("events/home/staff/see")
    else:
        form=RegistrationForm()

    return render(request, 'registration/login.html', {'form':form},RequestContext(request) )
# @method_decorator(login_required,name="dispatch")
# class RegisterEvent:
def get_eventregistrationform(request):
    if(request.method=='POST'):
        form=EventRegistrationForm(request.POST)
        if form.is_valid():
            eventid=form.cleaned_data['eventid']
            eventname=form.cleaned_data['eventname']
            description = form.cleaned_data['description']
            venue = form.cleaned_data['venue']
            date=form.cleaned_data['date']

            # department = form.cleaned_data['department']
            # section = form.cleaned_data['section']
            starttime=form.cleaned_data['starttime']
            endtime = form.cleaned_data['endtime']
            # cselab1= form.cleaned_data['CSE_Lab1']
            # cselab2 = form.cleaned_data['CSE_Lab2']
            # cselab3 = form.cleaned_data['CSE_Lab3']
            # cselab4 = form.cleaned_data['CSE_Lab4']
            # jcboseqeee = form.cleaned_data['JC_Bose_QEEE']
            # visweswarayya_conference = form.cleaned_data['Visweswarayya_Conference_Hall']
            # cclab1 = form.cleaned_data['CC_Lab1']
            # cclab2 = form.cleaned_data['CC_Lab2']
            res = form.cleaned_data['venue']
            resobj = Resources.objects.get(resource_name__iexact=res)
            rusage = ResourceUsage(date=date, resource=resobj, starttime=starttime, endtime=endtime)
            rusage.save()
            r = EventsList(eventname=eventname, eventid=eventid, venue=rusage, staffid=request.user, section="A", branch="CSE", description=description)
            r.save()
            return HttpResponseRedirect("/events/home/register_event/see")
    else:
        form=EventRegistrationForm()

    return render(request, 'registration/EventRegistration.html', {'form':form})



def resourceView(request):
    all_res = Resources.objects.all()
    context = []
    for resource in all_res:
        obj = {}
        obj['resource_name'] = resource.resource_name
        obj['starttime'] = "10:00"
        obj['endtime'] = "16.30"
        if ResourceUsage.objects.filter(date="2016-08-13", resource__resource_name__iexact=resource.resource_name):
            r=ResourceUsage.objects.get(date="2016-08-13",resource__resource_name__iexact=resource.resource_name)
            print r.starttime

            start=dt.time(10,00)



            end = dt.time(16, 30)
            if(start < r.starttime):
                obj['event_start_time']=r.starttime
            else:
                obj['event_start_time']="10:00"
            if(end > r.endtime):
                obj['event_end_time']=r.endtime
            else:
                obj['event_end_time']="16:30"


        context.append(obj)
    # res=ResourceUsage.objects.filter(date__exact=date)
    template = loader.get_template('FreeResources.html')
    result = template.render(context={"obj":context})
    return HttpResponse(result)






def homepage(request):
    template = loader.get_template('HomePage.html')
    result = template.render()
    return HTTPResponse(template)

def getEventList(request):
    events1=EventsList.objects.filter(facultyid=id)
    events2=EventsList.objects.all()
    template=loader.get_template('EventList.html')
    result=template.render(context={"mylist":events1,"list":events2})
    return HTTPResponse(result)

def cancelEvent(request):
    EventsList.objects.filter()


def getidcontent(request,id):

    eventslist=EventsList.objects.filter(staffid=id)

    template=loader.get_template('EventList.html')
    result=template.render(context={"eventslist":eventslist})
    return HttpResponse(result)


def editEvent(request,id):

    if (request.method == 'POST'):
        form = UpdateEventForm(request.POST)
        if form.is_valid():
            eventid = form.cleaned_data['eventid']
            eventname = form.cleaned_data['eventname']
            description = form.cleaned_data['description']
            venue = form.cleaned_data['venue']
            date = form.cleaned_data['date']

            # department = form.cleaned_data['department']
            # section = form.cleaned_data['section']
            starttime = form.cleaned_data['starttime']
            endtime = form.cleaned_data['endtime']
            # location=form.cleaned_data['location']

            # ID=form.cleaned_data['ID']


            # r=EventsList(eventname=eventname,staffid=12,eventid=eventid,venue=venue,description=description,section="A",branch="CSE",day=date.day,month=date.month,year=date.year,starthour=starttime.hour,startminute=starttime.minute,endhour=endtime.hour,endminute=endtime.minute)
            # r.save()
            # r = EventsList(eventname=eventname, staffid=Faculty.objects.get(staffid=request.user), eventid=eventid, venue=venue, description=description,section="A", branch="CSE",rating=5, day=date.day, month=date.month, year=date.year,starthour=starttime.hour, startminute=starttime.minute, endhour=endtime.hour,endminute=endtime.minute)
            # r = EventsList(eventname=eventname, staffid="1771", eventid=eventid, venue=venue, description=description,section="A", branch="CSE", rating=5, day=date.day, month=date.month, year=date.year,starthour=starttime.hour, startminute=starttime.minute, endhour=endtime.hour,endminute=endtime.minute)
            # r.save()
            eventslist = EventsList.objects.filter(eventid=id).update(eventname=eventname, staffid="1771", eventid=eventid, venue=venue, description=description,section="A", branch="CSE", rating=5, day=date.day, month=date.month, year=date.year,starthour=starttime.hour, startminute=starttime.minute, endhour=endtime.hour,endminute=endtime.minute)
            eventslist.save()
            return HttpResponseRedirect("/events/home/register_event/see")
    else:
        form = UpdateEventForm(id)

    return render(request, 'registration/EventRegistration.html', {'form': form})
