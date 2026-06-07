from rest_framework import serializers
from bms.models import Feeder, Log,Relay,Command
from authentication.serializers import PersonSerializer

class FeederSerializer(serializers.ModelSerializer):
    class Meta:
        model=Feeder
        fields=['id','name','get_absolute_url','get_delete_url','get_edit_url']
        
class RelaySerializer(serializers.ModelSerializer):
    class Meta:
        model=Relay
        fields=['id','name','state','color','get_absolute_url','get_delete_url','get_edit_url']
        
class CommandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Command
        fields=['id','ip','port','register','pin','value','name','color','get_absolute_url']

class RelayFullSerializer(serializers.ModelSerializer):
    commands=CommandSerializer(many=True)
    class Meta:
        model=Relay
        fields=['id','commands','state','name','get_absolute_url']

class FeederFullSerializer(serializers.ModelSerializer):
    relays=RelayFullSerializer(many=True)
    class Meta:
        model=Feeder
        fields=['id','name','relays','get_absolute_url']


        
class LogSerializer(serializers.ModelSerializer):
    person=PersonSerializer()
    relay=RelaySerializer()
    feeder=FeederSerializer()
    command=CommandSerializer()
    class Meta:
        model=Log
        fields=['id','person','title','relay','feeder','command','get_absolute_url','persian_date_added','persian_date_added_tag','succeed']
        