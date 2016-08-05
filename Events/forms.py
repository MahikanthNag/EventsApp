import datetime
from django.contrib.auth.models import User
from django.forms import forms, Form
from django import forms

from Events.models import *


class RegistrationForm(forms.Form):
    username=forms.CharField(max_length=30,label="username",required=True,error_messages={'invalid':'Username should be unique'})
    email=forms.EmailField(label="emailid",required=True)
    password1=forms.CharField(max_length=30,widget=forms.PasswordInput(),label="password",required=True)
    password2=forms.CharField(max_length=30,widget=forms.PasswordInput(),label="password(again)",required=True)
    ID=forms.CharField(max_length=30,required=True,error_messages={'invalid':'ID should not be Unique and Non Empty'})

    def clean_username(self):
        u=self.cleaned_data['username']
        try:
            u=User.objects.get(username__exact=u)
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("Username Already Exists . Please Try another name",code='invalid')
    def clean(self):
        p1=self.cleaned_data['password1']
        p2=self.cleaned_data['password2']
        if p1 is not None and p2 is not None:
            if p1 != p2:
                raise forms.ValidationError("Two passwords did not match")
            else:
                return self.cleaned_data
        else:
            raise forms.ValidationError("Both fields should match")




class EventRegistrationForm(forms.Form):
    eventname=forms.CharField(max_length=30,label="eventname",required=True,error_messages={'invalid':'Event Name should be unique'})
    eventid=forms.CharField(label="eventid",required=True,max_length=15)
    description=forms.CharField(max_length=500, label="description", required=True)
    # venue=forms.CharField(max_length=30, label="venue",required=True)
    # department=forms.ModelChoiceField(["CSE","IT"])
    date=forms.DateField()
    venue=forms.CharField(max_length=50)
    # venue = forms.ModelChoiceField(source=Resources.objects.values('resource_name'),description="enter resource")
    starttime=forms.TimeField()
    endtime=forms.TimeField()

    # CSE_Lab1 = forms.BooleanField(required=False)
    # CSE_Lab2 = forms.BooleanField(required=False)
    # CSE_Lab3 = forms.BooleanField(required=False)
    # CSE_Lab4 = forms.BooleanField(required=False)
    # Visweswarayya_Conference_Hall = forms.BooleanField(required=False)
    # JC_Bose_QEEE = forms.BooleanField(required=False)
    # CC_Lab1=forms.BooleanField(required=False)
    # CC_Lab2 = forms.BooleanField(required=False)


class UpdateEventForm(forms.Form):
    # eventname = forms.CharField(max_length=30, label="eventname", initial=EventsList.objects.values('eventname').filter(eventid=id),required=True,error_messages={'invalid': 'Event Name should be unique'})
    # eventid = forms.CharField(label="eventid",initial=id, required=True, max_length=15)
    # description = forms.CharField(max_length=500, initial=EventsList.objects.values('description').filter(eventid=id),label="description", required=True)
    # venue = forms.CharField(max_length=30, initial=EventsList.objects.values('venue').filter(eventid=id),label="venue", required=True)
    # # department=forms.ModelChoiceField(["CSE","IT"])
    # date = forms.DateField(initial=datetime.date.today)
    # # section=forms.ModelChoiceField(["A", "B"])
    # starttime = forms.TimeField()
    # endtime = forms.TimeField()
    eventname=forms.CharField(max_length=30,label="eventname",required=True,error_messages={'invalid':'Event Name should be unique'})
    eventid=forms.CharField(label="eventid",required=True,max_length=15)
    description=forms.CharField(max_length=500, label="description", required=True)
    venue=forms.CharField(max_length=30, label="venue",required=True)
    # department=forms.ModelChoiceField(["CSE","IT"])
    date=forms.DateField()
    # section=forms.ModelChoiceField(["A", "B"])
    starttime=forms.TimeField()
    endtime=forms.TimeField()


# class SettingsForm(forms.ModelForm):
#     receive_newsletter = forms.BooleanField()
#
#     class Meta:
#         model = Settings