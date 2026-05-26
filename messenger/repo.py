from messenger.serializers import MessageSerializer, NotificationSerializer
from authentication.serializers import PersonSerializer
import pusher
from django.db.models.query_utils import Q
from pusher.http import request_method
from authentication.repo import PersonRepo
from messenger.models import Member, Message,Channel, Notification

class NotificationRepo():
    def __init__(self,request,*args, **kwargs):        
        self.request = request
         
        self.objects = Notification.objects
        self.me=PersonRepo(request=self.request).me

    def add(self,*args, **kwargs):
        title=""
        body=''
        url=""
        icon=""
        profile_id=""
        color=""
        priority=""
        if 'title' in kwargs:
            title=kwargs['title']
        if 'body' in kwargs:
            body=kwargs['body']
        if 'url' in kwargs:
            url=kwargs['url']
        if 'icon' in kwargs:
            icon=kwargs['icon']
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
        if 'color' in kwargs:
            color=kwargs['color']
        if 'priority' in kwargs:
            priority=kwargs['priority']



class MessageRepo:
    def __init__(self,request,*args, **kwargs):
        self.request = request
         
        self.objects = Message.objects
        self.me=PersonRepo(request=request).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'channel_id' in kwargs:
            objects=objects.filter(channel_id=kwargs['channel_id'])
        if 'for_home' in kwargs:
            objects=objects.all()
        return objects
    def message(self,*args, **kwargs):
        pk=0
        if 'message_id' in kwargs:
            pk=kwargs['message_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def send_message(self,*args, **kwargs):
        message=self.message(*args, **kwargs)
        if message is not None:
            message_title=message.title
            message_body=message.body
            channel=message.channel
            event=message.event
        else:
            message_title=kwargs['message_title']
            message_body=kwargs['message_body']
            channel_id=kwargs['channel_id']
            event=kwargs['event']
            channel=ChannelRepo(request=self.request).channel(channel_id=channel_id)
        
        message=Message()
        message.channel=channel
        message.event=event
        message.title=message_title
        message.body=message_body
        message.sender=PersonRepo(request=self.request).me
        message.save()
        
        if channel is None:
            return
        pusher_client = pusher.Pusher(
            app_id=channel.app_id,
            key=channel.key,
            secret=channel.secret,
            cluster=channel.cluster,
            ssl=True
            )
        # import json
        # sender=(PersonSerializer(message.sender).data)
        # message_object={'sender':sender,'title':message.title,'body':message.body}
        message_object=MessageSerializer(message).data
        pusher_client.trigger(channel.channel_name, event, message_object)
        return message




class NotificationRepo:
    def __init__(self,request,*args, **kwargs):        
        self.request = request
         
        self.objects = Notification.objects
        self.me=PersonRepo(request=self.request).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'member_id' in kwargs:
            objects=objects.filter(member_id=kwargs['member_id'])
        if 'read' in kwargs:
            objects=objects.filter(read=kwargs['read'])
        return objects
    def notification(self,*args, **kwargs):
        if 'notification_id' in kwargs:
            pk=kwargs['notification_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        notification= self.objects.filter(pk=pk).first()
        if 'read' in kwargs:
            notification.read=kwargs['read']
            notification.save()
        return notification
    
    def send_notification(self,*args, **kwargs):
        member=MemberRepo(request=self.request).member(*args, **kwargs)
        if member is None:
            return
        message_title=kwargs['message_title']
        message_body=kwargs['message_body']
        event=member.event
        channel=ChannelRepo(request=self.request).channel(channel_id=member.channel.id)
        
        notification=Notification()
        notification.channel=channel
        notification.event=event
        notification.member=member
        notification.title=message_title
        notification.body=message_body
        notification.sender=PersonRepo(request=self.request).me
        notification.save()
        
        if channel is None:
            return
        pusher_client = pusher.Pusher(
            app_id=channel.app_id,
            key=channel.key,
            secret=channel.secret,
            cluster=channel.cluster,
            ssl=True
            )
        # import json
        # sender=(PersonSerializer(message.sender).data)
        # message_object={'sender':sender,'title':message.title,'body':message.body}
        message_object=NotificationSerializer(notification).data
        pusher_client.trigger(channel.channel_name, event, message_object)
        return notification

 


class ChannelRepo:
    def __init__(self,request,*args, **kwargs):        
        self.request = request
         
        self.objects = Channel.objects
        self.me=PersonRepo(request=self.request).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'for_home' in kwargs:
            objects=objects
        return objects.all()
    def channel(self,*args, **kwargs):
        if 'channel_id' in kwargs:
            pk=kwargs['channel_id']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()



class MemberRepo:
    def __init__(self,request,*args, **kwargs):        
        self.request = request
         
        self.objects = Member.objects
        self.me=PersonRepo(request=self.request).me
    def list(self,*args, **kwargs):
        objects=self.objects.all()
        if 'for_home' in kwargs:
            objects=objects
        return objects.all()
    def member(self,*args, **kwargs):
        pk=0
        if 'member_id' in kwargs:
            pk=kwargs['member_id']
        if 'member' in kwargs:
            return kwargs['member']
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()


