from rest_framework import serializers
from Events.models import *

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsList
        fields = ('eventid','eventname','staffid','description','venue','day','month','year','rating')