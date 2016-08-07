from Tkinter import _stringify

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
# Create your views here.
from django.template.context import RequestContext

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



def get_eventregistrationform(request):
    if(request.method=='POST'):
        form=EventRegistrationForm(request.POST)
        if form.is_valid():
            eventid=form.cleaned_data['eventid']
            eventname=form.cleaned_data['eventname']
            description = form.cleaned_data['description']
            date=form.cleaned_data['date']

            # department = form.cleaned_data['department']
            # section = form.cleaned_data['section']
            starttime=form.cleaned_data['starttime']
            endtime = form.cleaned_data['endtime']

            res = form.cleaned_data['venue']
            resobj = Resources.objects.get(resource_name__iexact=res)
            # check={'one':0}
            r = ResourceUsage.objects.filter(date=date, resource__resource_name__iexact=res)
            for res in r:

                if(res.starttime<=starttime and starttime<=res.endtime) or (res.endtime>=endtime and res.starttime<=endtime):
                    # check['one']=1
                    return render(request, 'Error.html')



            rusage = ResourceUsage(date=date, resource=resobj, starttime=starttime, endtime=endtime)
            rusage.save()
            r = EventsList(eventname=eventname, eventid=eventid, venue=rusage, staffid=request.user, section="A", branch="CSE", description=description)
            r.save()
            return HttpResponseRedirect("/events/home/register_event/see")
    else:
        form=EventRegistrationForm()

    return render(request, 'registration/EventRegistration.html', {'form':form})


# def dashboard(request):
#     template = loader.get_template('HomePage.html')
#     result = template.render()
#     return HttpResponse(result)


# def resourceView(request):
#     all_res = Resources.objects.all()
#     context1 = []
#     obj = {}
#     for resource in all_res:
#
#         obj['resource_name'] = resource.resource_name
#         obj['starttime'] = "10:00"
#         obj['endtime'] = "16.30"
#         obj['event_start_time']="none"
#         obj['event_end_time'] = "none"
#         # if ResourceUsage.objects.filter(date="2016-08-12", resource__resource_name__iexact=resource.resource_name):
#         #     r=ResourceUsage.objects.get(date="2016-08-12",resource__resource_name__iexact=resource.resource_name)
#         r = ResourceUsage.objects.filter(date="2016-08-12", resource__resource_name__iexact=resource.resource_name)
#         obj['starttime'] = "changed"
#         for res in r:
#
#             obj['starttime']="changed"
#             start=dt.time(10,00)
#
#
#
#             end = dt.time(16, 30)
#             if(start < res.starttime):
#                 obj['event_start_time']=res.starttime.__str__()
#             else:
#                 obj['event_start_time']="10:00"
#             if(end > res.endtime):
#                 obj['event_end_time']=res.endtime.__str__()
#             else:
#                 obj['event_end_time']="16:30"
#
#
#             context1.append(obj)
#     # res=ResourceUsage.objects.filter(date__exact=date)
#     # template = loader.get_template('FreeResources1.html')
#     # result = template.render()
#     return render(request, 'FreeResources1.html', {'obj': context1})

def resourceview(request):
    all_res = Resources.objects.all()
    context1 = []
    obj = {}
    flag=0
    i=0
    for i in range(0, 100):
        context1.append({})
    i = 0

    for resource in all_res:
        flag=0
        context1[i]['resource_name'] = resource.resource_name
        context1[i]['starttime'] = dt.time(10,00).__str__()
        context1[i]['endtime'] = dt.time(16,30).__str__()
                # if ResourceUsage.objects.filter(date="2016-08-12", resource__resource_name__iexact=resource.resource_name):
        #     r=ResourceUsage.objects.get(date="2016-08-12",resource__resource_name__iexact=resource.resource_name)
        r = ResourceUsage.objects.filter(date="2016-08-12", resource__resource_name__iexact=resource.resource_name)

        for res in r:

            flag=1
            start=dt.time(10,00)



            end = dt.time(16, 30)
            if(start < res.starttime):
                context1[i]['event_start_time']=res.starttime.__str__()
            else:
                context1[i]['event_start_time']=dt.time(10,00).__str__()
            if(end > res.endtime):
                context1[i]['event_end_time']=res.endtime.__str__()
            else:
                context1[i]['event_end_time']=dt.time(16,30).__str__()
            i=i+1

            context1.append(obj)
        if flag==0:
            context1[i]['event_start_time']=dt.time(12,00)
            context1[i]['event_end_time']=dt.time(12,00)
            i=i+1
            # context1.append(obj)
    # res=ResourceUsage.objects.filter(date__exact=date)
    # template = loader.get_template('FreeResources1.html')
    # result = template.render()
    return render(request, 'FreeResources1.html', {'obj': context1})


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
