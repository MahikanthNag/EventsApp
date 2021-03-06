import user
from unittest.case import _UnexpectedSuccess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import request
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DetailView
from django.utils import timezone
from django.views.generic.edit import DeleteView
from rest_framework.urls import template_name

from Events.forms import UpdateEventForm, UpdateEventForm1
from Events.models import *
from django.views.generic.list import ListView
from django.views import *

class Dashboard(ListView):
    template_name = 'Dashboard.html'

    def get_queryset(self):
        user = self.request.user
        return EventsList.objects.values('eventname', 'description')
class EndEvent(ListView):
    pass

@method_decorator(login_required,name="dispatch")
class eventslist(ListView):
    model=EventsList
    template_name = 'EventList.html'
    context_object_name = 'eventslist'

    def get_queryset(self):

            user=self.request.user
            events = EventsList.objects.values('id', 'eventname', 'description', 'venue__date','venue__resource__resource_name','venue__starttime','venue__endtime')

            for e in events: e['venue__date'] = e['venue__date'].strftime('%Y-%m-%d')
            uniques = []
            uniqueids = set([x['id'] for x in events])
            for uid in uniqueids:
                objs = [x for x in events if uid == x['id']]
                d = objs[0]
                for o in objs:
                    d['venue__resource__resource_name'] += (", " + o['venue__resource__resource_name'])
                uniques.append(d)
            return uniques

class dashboard(ListView):
    model = EventsList
    template_name = 'HomePage.html'
    context_object_name = 'eventslist'

    def get_queryset(self):
        user = self.request.user
        events = EventsList.objects.values('id', 'eventname', 'description', 'venue__date', 'venue__resource__resource_name')
        for e in events: e['venue__date'] = e['venue__date'].strftime('%Y-%m-%d')
        uniques = []
        uniqueids = set([x['id'] for x in events])
        for uid in uniqueids:
            objs = [x for x in events if uid == x['id']]
            d = objs[0]
            for o in objs:
                d['venue__resource__resource_name'] += (", " + o['venue__resource__resource_name'])
            uniques.append(d)
        return uniques



                    # return EventsList.objects.values('eventid', 'eventname', 'description')

# class LoginPage():
#
#     template_name='login.html'



class facultylist(ListView):
    model=EventsList
    template_name = 'facultylist.html'
    context_object_name = 'facultydata'


    def get_queryset(self):

        return User.objects.values('id', 'first_name', 'email')



class UpdateEvent(ListView):
    model=EventsList
    template_name="EventUpdation.html"
    context_object_name = 'facultydata'
    # def editEvent(request, id):


    def get_queryset(self):
        id = self.kwargs.get('id')
        if (request.method == 'POST'):
            form = UpdateEventForm(request.POST)
            if form.is_valid():
                eventname = form.cleaned_data['eventname']
                description = form.cleaned_data['description']
                venue = form.cleaned_data['venue']
                date = form.cleaned_data['date']

                # department = form.cleaned_data['department']
                # section = form.cleaned_data['section']
                starttime = form.cleaned_data['starttime']
                endtime = form.cleaned_data['endtime']

                # r=EventsList(eventname=eventname,staffid=12,eventid=eventid,venue=venue,description=description,section="A",branch="CSE",day=date.day,month=date.month,year=date.year,starthour=starttime.hour,startminute=starttime.minute,endhour=endtime.hour,endminute=endtime.minute)
                # r.save()
                # r = EventsList(eventname=eventname, staffid=Faculty.objects.get(staffid=request.user), eventid=eventid, venue=venue, description=description,section="A", branch="CSE",rating=5, day=date.day, month=date.month, year=date.year,starthour=starttime.hour, startminute=starttime.minute, endhour=endtime.hour,endminute=endtime.minute)
                # r = EventsList(eventname=eventname, staffid="1771", eventid=eventid, venue=venue, description=description,section="A", branch="CSE", rating=5, day=date.day, month=date.month, year=date.year,starthour=starttime.hour, startminute=starttime.minute, endhour=endtime.hour,endminute=endtime.minute)
                # r.save()
                eventslist = EventsList.objects.filter(pk=id).update(eventname=eventname, staffid="1771",
                                                                          venue=venue,
                                                                          description=description, section="A",
                                                                          branch="CSE", rating=5, day=date.day,
                                                                          month=date.month, year=date.year,
                                                                          starthour=starttime.hour,
                                                                          startminute=starttime.minute,
                                                                          endhour=endtime.hour,
                                                                          endminute=endtime.minute)
                eventslist.save()
                HttpResponseRedirect("/events/home/register_event/see")
        else:
            form = UpdateEventForm()
            # def get_queryset(self):
            #     eventid=self.kwargs.get('id')

class EventUpdate(UpdateView):
    model = EventsList
    form_class = UpdateEventForm1
    template_name = 'event_update.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect("/events/home/register_event/see")



class EventDetailView(DetailView):
    model = EventsList
    template_name = 'event_detail.html'
    # def get_context_data(self, **kwargs):
    #     context = super(EventDetailView, self).get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

    context_object_name = 'object'
    queryset =EventsList.objects.values('id', 'eventname', 'description', 'venue__date','venue__resource__resource_name',
                                        'venue__starttime','venue__endtime', 'resourceperson', 'res_person_workplace', 'staffid__first_name')

class EventDeleteView(DeleteView):
    model = EventsList
    template_name = 'eventslist_confirm_delete.html'
    success_url = '/events/home/'