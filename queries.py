import os

from django.core.wsgi import get_wsgi_application
from django.db.models import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled9.settings")

application = get_wsgi_application()
from Events.models import *
import datetime as dt
# q=Faculty.objects.all()
# print q
end = dt.time(16, 30)
q=EventsList.objects.values('eventid','eventname','description')
q=EventsList.objects.values('eventid','eventname','description').filter(staffid="1")
# q=EventsList.objects.values('eventid','eventname','description').filter(staffid=Faculty.objects.get(staffid="1"))
# q=Faculty.objects.values('staffid').get(staffid="1234")
# q=Faculty.objects.values('').get(staffid="1234")
# q=(True==Settings.objects.values_list('CSE_Lab1').latest('id')[0])
q=ResourceUsage.objects.filter(date="2016-08-12", resource__resource_name__iexact="CSE Lab1")
r = ResourceUsage.objects.filter(date="2016-08-12", resource__resource_name__iexact="CSE Lab1")


# for res in all_res:
#     print res.resource_name
# context1=[]
# obj={}
# for resource in all_res:
#
#         obj['resource_name'] = resource.resource_name
#         obj['starttime'] = "10:00"
#         obj['endtime'] = "16.30"
#         # obj['event_start_time']="none"
#         # obj['event_end_time'] = "none"
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
# # print all_res[1].resource_name
# print context1

r = ResourceUsage.objects.filter(date="2016-08-12", resource__resource_name__iexact="CSE Lab1")
for res in r:

    print res.starttime
    print res.endtime