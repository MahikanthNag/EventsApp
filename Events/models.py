from __future__ import unicode_literals

from datetime import datetime
from time import time, localtime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
#Students Model to be stored as a table in mysql database
class Students(models.Model):
    name=models.CharField(max_length=30)
    rollno=models.CharField(max_length=20)
    password=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Resources(models.Model):
    resource_name=models.CharField(max_length=50)

    def __str__(self):
        return self.resource_name


class ResourceUsage(models.Model):
    resource=models.ForeignKey(Resources)
    date = models.DateField(default=datetime.today())
    starttime = models.TimeField(blank=True)
    endtime = models.TimeField(blank=True)


class EventsList(models.Model):
    eventid=models.CharField(max_length=20)
    eventname=models.CharField(max_length=30)
    staffid=models.ForeignKey(User)
    year=models.IntegerField(default=0)
    branch=models.CharField(max_length=6,default='select')
    section = models.CharField(max_length=6,default='select')
    description=models.CharField(max_length=1000)
    venue=models.ForeignKey(ResourceUsage)
    resourceperson=models.CharField(max_length=30,default="NULL")
    res_person_workplace=models.CharField(max_length=30,default="NULL")


    def __str__(self):
        return self.eventname


class Feedback(models.Model):
    rating=models.IntegerField(default=0)
    event=models.ForeignKey(EventsList)

# TODO: A: Gropup by and count queries
# TODO: M: dropdown.
# TODO: Calendar API