from authentication.serializers import PersonSerializer
from messenger.models import Channel, Member, Message
from rest_framework import serializers
from authentication.models import Person

class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields=['id','full_name','image','get_absolute_url']
        
class MessageSerializer(serializers.ModelSerializer):
    sender=SenderSerializer()
    class Meta:
        model = Message
        fields=['id','title','body','sender','perisan_date_send','get_absolute_url','get_delete_url','get_edit_url']
        
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields=['id','name','key','cluster']
        
class MemberSerializer(serializers.ModelSerializer):
    channel=ChannelSerializer()
    person=PersonSerializer()
    class Meta:
        model = Member
        fields=['id','event','person','channel']
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields=['id','title','body','get_absolute_url']