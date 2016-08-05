import os

from django.core.wsgi import get_wsgi_application
from django.db.models import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "untitled9.settings")

application = get_wsgi_application()
from Events.models import *

# q=Faculty.objects.all()
# print q

q=EventsList.objects.values('eventid','eventname','description')
q=EventsList.objects.values('eventid','eventname','description').filter(staffid="1")
# q=EventsList.objects.values('eventid','eventname','description').filter(staffid=Faculty.objects.get(staffid="1"))
# q=Faculty.objects.values('staffid').get(staffid="1234")
# q=Faculty.objects.values('').get(staffid="1234")
q=(True==Settings.objects.values_list('CSE_Lab1').latest('id')[0])
print q