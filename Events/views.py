from Tkinter import _stringify
import smtplib
import mimetypes
import django
from email.mime.multipart import MIMEMultipart
from email import encoders
from django.db.models import *
from django.template import loader
from email.message import Message
from django.core.wsgi import get_wsgi_application
from django.core.mail import EmailMultiAlternatives
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import urllib
import os

from django.core.wsgi import get_wsgi_application
from django.db.models import *
from httpie.models import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
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
            res_string=""
            # for res_individual in res:
            #     res_string=res_string+res_individual
            rusage=[]


            i=0
            for res_individual in res:
                resobj = Resources.objects.get(resource_name__iexact=res_individual)
                r = ResourceUsage.objects.filter(date=date, resource__resource_name__iexact=res_individual)

                for res1 in r:

                    if (res1.starttime <= starttime and starttime <= res1.endtime) or (
                                    res1.endtime >= endtime and res1.starttime <= endtime):
                        obj = resourceview(date)
                        return render(request, 'Error.html', context={'date': date, 'obj': obj})

                rusage.append(ResourceUsage(date=date, resource=resobj, starttime=starttime, endtime=endtime))


            for rus in rusage:
                rus.save()

            check = EventsList.objects.filter(venue__date=date, branch=branch)
            if check:
                if check[0].section == "both":
                    messages.error(request, "This branch has another event on this date.")
                if check[0].section == section:
                    messages.error(request, "This section has another event on this date.")
                return render(request, 'registration/EventRegistration.html', {'form': form})

            if date.__str__() < dt.datetime.today().__str__():
                messages.error(request, "Cannot register on a past date.")
                return render(request, 'registration/EventRegistration.html', {'form': form})


            r = EventsList(eventname=eventname, staffid=request.user,
                           section=section, branch=branch, description=description,resourceperson=resourceperson,
                           res_person_workplace=res_person_workplace,year=int(year))
            r.save()

            for venue_usage in rusage:
                r.venue.add(venue_usage)


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







def resview(request,date1):
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
    template = loader.get_template('FreeResources1.html')
    result = template.render(context={"obj":context1})
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

    eventslist=EventsList.objects.filter(staffid=id).values('eventname','venue__resource__resource_name', 'venue__date','id','venue__endtime','venue__starttime'
                                                            ,'resourceperson','res_person_workplace','staffid__first_name')
    for e in eventslist: e['venue__date'] = e['venue__date'].strftime('%Y-%m-%d')

    uniques = []
    uniqueids = set([x['id'] for x in eventslist])
    for uid in uniqueids:
        objs = [x for x in eventslist if uid == x['id']]
        d = objs[0]
        for o in objs:
            d['venue__resource__resource_name'] += (", " + o['venue__resource__resource_name'])
        uniques.append(d)


    template=loader.get_template('EventList.html')
    result=template.render(context={"eventslist":uniques})
    return HttpResponse(result)

def geteventcontent(request,id):

    eventslist=EventsList.objects.filter(pk=id).values('eventname', 'venue__date','id','venue__endtime','venue__starttime'
                                                            ,'resourceperson','res_person_workplace','staffid__first_name',
                                                       'venue__resource__resource_name', 'description', 'staffid__username')
    for e in eventslist: e['venue__date'] = e['venue__date'].strftime('%Y-%m-%d')
    eventslist[0]['own'] = False
    for e in range(1, eventslist.__len__()):
        eventslist[0]['venue__resource__resource_name'] += ", " + eventslist[e]['venue__resource__resource_name']
    if request.user.username == eventslist[0]['staffid__username']:
        eventslist[0]['own'] = True
    template=loader.get_template('event_detail.html')
    result=template.render(context={"object":eventslist[0]})
    return HttpResponse(result)


def editEvent(request,id):

    if (request.method == 'POST'):
        form = UpdateEventForm1(request.POST)
        if form.is_valid():
            eventname = form.cleaned_data['eventname']
            description = form.cleaned_data['description']
            resourceperson = form.cleaned_data['resourceperson']
            res_work = form.cleaned_data['res_person_workplace']
            date = form.cleaned_data['date']
            branch = form.cleaned_data['branch']
            section = form.cleaned_data['section']
            starttime = form.cleaned_data['starttime']
            endtime = form.cleaned_data['endtime']

            res = form.cleaned_data['venue']

            for res2 in res:
                r=Resources.objects.get(resource_name=res2)
                res3=ResourceUsage.objects.filter(date=date)
                    # for x in res3:
                    #     x.delete()
                for res1 in res3:
                    if res1.resource==res2:
                        if (res1.starttime <= starttime and starttime <= res1.endtime) or (
                                        res1.endtime >= endtime and res1.starttime <= endtime):
                            obj = resourceview(date)
                            return render(request, 'Error.html', context={'date': date, 'obj': obj})

            resusageobj=[]
            for res_individual in res:

                resobj = Resources.objects.get(resource_name__iexact=res_individual)
                # resusageobj = EventsList.objects.get(pk=id).venue


                resusageobj.append(ResourceUsage(resource=resobj))

            eventlist = EventsList.objects.get(pk=id)
            eventlist.venue.clear()
            # ResourceUsage.objects.filter(date=date,).delete()
            for rusage in resusageobj:



                rusage.date = date
                rusage.starttime = starttime
                rusage.endtime = endtime
                rusage.save()

                eventlist.venue.add(rusage)

            # resusageobj.save()


            eventlist.description = description
            eventlist.eventname = eventname
            eventlist.branch = branch
            eventlist.section = section
            eventlist.resourceperson = resourceperson
            eventlist.res_person_workplace = res_work


            eventlist.save()
            return HttpResponseRedirect("/events/home/register_event/see")
    else:

        form = UpdateEventForm1(initial=EventsList.objects.filter(pk=id).values()[0])

    return render(request, 'event_update.html', {'form': form})



def sendMail(request,id,emailid,password,to_email):

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled9.settings")

    application = get_wsgi_application()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled9.settings")

    emailfrom = emailid
    emailto = to_email
    fileToSend = "sam.txt"
    username=emailid[:emailid.find("@")]
    # username = "babanag95"
    password = password

    msg = MIMEMultipart()
    msg["From"] = emailid
    msg["To"] = to_email
    msg["Subject"] = "sub"
    # msg.preamble = "help I cannot send an attachment to save my life"

    # ctype, encoding = mimetypes.guess_type(fileToSend)
    # if ctype is None or encoding is not None:
    #     ctype = "application/octet-stream"

    # maintype, subtype = ctype.split("/", 1)



    eventslist = EventsList.objects.filter(pk=id).values('eventname', 'venue__date', 'id', 'venue__endtime',
                                                         'venue__starttime'
                                                         , 'resourceperson', 'res_person_workplace',
                                                         'staffid__first_name',
                                                         'venue__resource__resource_name', 'description',
                                                         'staffid__username')


    for e in eventslist: e['venue__date'] = e['venue__date'].strftime('%Y-%m-%d')
    eventslist[0]['own'] = False
    for e in range(1, eventslist.__len__()):
        eventslist[0]['venue__resource__resource_name'] += ", " + eventslist[e]['venue__resource__resource_name']
    if request.user.username == eventslist[0]['staffid__username']:
        eventslist[0]['own'] = True
    template = loader.get_template('event_detail.html')
    result = template.render(context={"object": eventslist[0]})



    # HTTPResponse(result)
    # part = MIMEApplication(open(str("graph.svg"), "rb").read())
    part = MIMEText(result, 'html')
    msg.attach(part)
    part.add_header('Content-Disposition', 'attachment')
    msg.attach(part)


    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username, password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()