from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from Events import views,classviews
from django.db.models import *


urlpatterns=[

    # url(r'^staff/(?P<id>[A-Za-z0-9]+)',views),
    url(r'^$',classviews.Dashboard.as_view(),name='dashboard'),
    url(r'^register_event/see/(?P<pk>[A-Za-z0-9 -]+)/$',classviews.EventDetailView.as_view(),name='eventdetail'),
    url(r'^register_event/see/$',classviews.eventslist.as_view(),name='eventdata'),
    url(r'^register_event/$',login_required(views.get_eventregistrationform),name="event_registration"),
    url(r'^staff/(?P<id>[A-Za-z0-9 -]+)/view_events',views.getidcontent,name='eventslist'),
    url(r'^staff/all/$',classviews.facultylist.as_view(),name='facultydata'),
    url(r'^logout1$',views.logout1,name="logout"),
    url(r'^edit/(?P<pk>[A-Za-z0-9 -]+)',classviews.EventUpdate.as_view(),name="edit_event"),
    url(r'^end/(?P<pk>[A-Za-z0-9 -]+)',classviews.EndEvent.as_view(),name="end_event"),
    url(r'^resources',views.resourceview),

    #
    # url(r'^event_snippets/$',views.snippet_list),
    # url(r'^event_snippets/(?P<eventid>([A-Za-z0-9]|-)+)',views.snippet_detail),

]