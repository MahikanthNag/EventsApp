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
from django.contrib import messages
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
            year=form.cleaned_data['year']

            description = form.cleaned_data['description']
            date=form.cleaned_data['date']

            branch= form.cleaned_data['branch']
            section = form.cleaned_data['section']
            starttime=form.cleaned_data['starttime']
            endtime = form.cleaned_data['endtime']
            resourceperson=form.cleaned_data['resourceperson']
            res_person_workplace=form.cleaned_data['res_person_workplace']

            res = form.cleaned_data['venue']
            resobj = Resources.objects.get(resource_name__iexact=res)
            # check={'one':0}
            r = ResourceUsage.objects.filter(date=date, resource__resource_name__iexact=res)

            check=EventsList.objects.filter(venue__date=date,branch=branch)
            if check:
                if check[0].section=="both":
                    messages.error(request, "This branch has another event on this date.")
                if check[0].section == section:
                    messages.error(request, "This section has another event on this date.")
                return render(request, 'registration/EventRegistration.html', {'form': form})

            if date.__str__() < dt.datetime.today().__str__():
                messages.error(request, "Cannot register on a past date.")
                return render(request, 'registration/EventRegistration.html', {'form': form})

            for res in r:

                if(res.starttime<=starttime and starttime<=res.endtime) or (res.endtime>=endtime and res.starttime<=endtime):
                    obj = resourceview(date)
                    return render(request, 'Error.html', context={'date':date, 'obj':obj})

            rusage = ResourceUsage(date=date, resource=resobj, starttime=starttime, endtime=endtime)
            rusage.save()
            r = EventsList(eventname=eventname, eventid=eventid, venue=rusage, staffid=request.user,
                           section=section, branch=branch, description=description,resourceperson=resourceperson,
                           res_person_workplace=res_person_workplace,year=int(year))
            r.save()
            return HttpResponseRedirect("/events/home/register_event/see")
    else:
        form=EventRegistrationForm()

    return render(request, 'registration/EventRegistration.html', {'form':form})

def resourceview(date1):
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
        r = ResourceUsage.objects.filter(date=date1, resource__resource_name__iexact=resource.resource_name)

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
    return context1


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

    eventslist=EventsList.objects.filter(staffid=id).values('eventid', 'eventname', 'venue__date','id','venue__endtime','venue__starttime'
                                                            ,'resourceperson','res_person_workplace','staffid__first_name')
    for e in eventslist: e['venue__date'] = e['venue__date'].strftime('%Y-%m-%d')
    template=loader.get_template('EventList.html')
    result=template.render(context={"eventslist":eventslist})
    return HttpResponse(result)

def geteventcontent(request,id):

    eventslist=EventsList.objects.filter(pk=id).values('eventname', 'venue__date','id','venue__endtime','venue__starttime'
                                                            ,'resourceperson','res_person_workplace','staffid__first_name',
                                                       'venue__resource__resource_name', 'description', 'staffid__username')
    for e in eventslist: e['venue__date'] = e['venue__date'].strftime('%Y-%m-%d')
    eventslist[0]['own'] = False
    if request.user.username == eventslist[0]['staffid__username']:
        eventslist[0]['own'] = True
    template=loader.get_template('event_detail.html')
    result=template.render(context={"object":eventslist[0]})
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

            eventslist = EventsList.objects.filter(eventid=id).update(eventname=eventname, staffid="1771", eventid=eventid, venue=venue, description=description,section="A", branch="CSE", rating=5, day=date.day, month=date.month, year=date.year,starthour=starttime.hour, startminute=starttime.minute, endhour=endtime.hour,endminute=endtime.minute)
            eventslist.save()
            return HttpResponseRedirect("/events/home/register_event/see")
    else:
        form = UpdateEventForm(id)

    return render(request, 'event_update.html', {'form': form})
