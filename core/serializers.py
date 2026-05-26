from rest_framework import serializers
from .models import Page,Event
from authentication.serializers import PersonSerializer

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','title','thumbnail','app_name','class_title','get_absolute_url' ,'get_edit_url','get_delete_url']
 

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['id','thumbnail','title','persian_'+'event_datetime','persian_'+'end_datetime','persian_'+'start_datetime','get_absolute_url' ,'get_edit_url','get_delete_url']
 
class PageBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','title','app_name','class_title','get_edit_url','get_delete_url', 'thumbnail','get_absolute_url' ]
 
