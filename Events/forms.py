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
    resourceperson=forms.CharField(max_length=30,required=True,error_messages={'invalid':'Resource Person should not be Unique and Non Empty'})
    res_person_workplace=forms.CharField(max_length=30,required=False)
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
    description=forms.CharField(max_length=500, label="description", required=True)
    year=forms.ChoiceField(choices=[('1','1'),('2','2'),('3','3'),('4','4')])
    resourceperson=forms.CharField(max_length=30,required = True)

    res_person_workplace=forms.CharField(max_length=100,required=True)
    branch=forms.ChoiceField(choices=[('CSE','CSE'),('IT','IT'),('ECE','ECE'),('EEE','EEE')])
    section=forms.ChoiceField(choices=[('A','A'),('B','B'),('both','both')])
    date=forms.DateField()
    venue = forms.ModelMultipleChoiceField(queryset=Resources.objects.all(),widget=forms.SelectMultiple)
    starttime=forms.TimeField()
    endtime=forms.TimeField()


class UpdateEventForm(forms.Form):
    eventname=forms.CharField(max_length=30,label="eventname",required=True,error_messages={'invalid':'Event Name should be unique'})
    description = forms.CharField(max_length=500, label="description", required=True)
    year = forms.ChoiceField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')])
    resourceperson = forms.CharField(max_length=30, required=True)
    res_person_workplace = forms.CharField(max_length=100, required=True)
    branch = forms.ChoiceField(choices=[('CSE', 'CSE'), ('IT', 'IT'), ('ECE', 'ECE'), ('EEE', 'EEE')])
    section = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('both', 'both')])
    date = forms.DateField()
    venue = forms.ModelMultipleChoiceField(queryset=Resources.objects.all(), widget=forms.SelectMultiple)
    starttime = forms.TimeField()
    endtime = forms.TimeField()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('instance')
        self.instance = request
        super(UpdateEventForm, self).__init__(*args, **kwargs)


class UpdateEventForm1(forms.ModelForm):
    class Meta:
        model = EventsList
        fields = ['eventname', 'description', 'resourceperson', 'res_person_workplace']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', '')
        super(UpdateEventForm1, self).__init__(*args, **kwargs)
        self.fields['branch'] = forms.ChoiceField(choices=[('CSE', 'CSE'), ('IT', 'IT'), ('ECE', 'ECE'), ('EEE', 'EEE')])
        self.fields['section'] = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('both', 'both')])
        self.fields['date'] = forms.DateField()
        self.fields['venue'] = forms.ModelMultipleChoiceField(queryset=Resources.objects.all(),widget=forms.SelectMultiple)
        self.fields['starttime'] = forms.TimeField()
        self.fields['endtime'] = forms.TimeField()