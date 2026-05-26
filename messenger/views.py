from authentication.repo import PersonRepo
from messenger.enums import ParameterEnum
from messenger.serializers import MemberSerializer,NotificationSerializer
from messenger.repo import MemberRepo, MessageRepo,ChannelRepo,NotificationRepo
from django.shortcuts import render
from utility.repo import ParameterRepo
from messenger.apps import APP_NAME
from django.views import View
from core.views import CoreContext,leolog
from phoenix.settings import PUSHER_IS_ENABLE
import json

TEMPLATE_ROOT=APP_NAME+"/"
LAYOUT_PARENT='phoenix/layout.html'

def MessengerContext(request,*args, **kwargs):
    context={}
    if 'me_person' in kwargs and kwargs['me_person'] is not None:
        me_person=kwargs['me_person']
    else:
        me_person=PersonRepo(request=request).me
        if me_person is None:
            context['PUSHER_IS_ENABLE']=False
            return {}
    # PUSHER_IS_ENABLE=ParameterRepo(request=request,app_name=APP_NAME).parameter(name=ParameterEnum.PUSHER_IS_ENABLE,default='False').boolean_value
    if PUSHER_IS_ENABLE and me_person is not None and me_person.member_set.first() is not None:
        context.update(MemberContext(request=request))
        # context['PUSHER_IS_ENABLE'] = True
        
    else:
        context['PUSHER_IS_ENABLE'] = False

    return context

    return context
def MemberContext(request,*args, **kwargs):
    context={}
    if 'member' in kwargs:
        member=kwargs['member']
    elif 'member_id' in kwargs:
        member=MemberRepo(request=request).member(*args, **kwargs)
    if 'me_person' in kwargs:
        me_person=kwargs['me_person']
        member=me_person.member_set.first()
    elif 'me_person_id' in kwargs:
        me_person=PersonRepo(request=request).me_person(*args, **kwargs)
        member=me_person.member_set.first()
    else:
        me_person=PersonRepo(request=request).me
        member=me_person.member_set.first()
    
    if member is not None:
        context['member']=member
        context['member_s']=json.dumps(MemberSerializer(member).data)
        channels=[]
        context['channels']=channels

        
        notifications=NotificationRepo(request=request).list(member_id=context['member'].id,read=False)
        if len(notifications)>0:
            notifications_s=json.dumps(NotificationSerializer(notifications,many=True).data)
            context['notifications_s']=notifications_s
            context['notifications']=notifications

    return context


def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    me_person=PersonRepo(request=request).me
    context.update(MessengerContext(request=request,me_person=me_person))
    return context
    
class HomeViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        channels=ChannelRepo(request=request).list(*args, **kwargs)
        context['channels']=channels

        
        # events=EventRepo(request=request).list(for_home=True,*args, **kwargs)
        # context['events']=events

        
        return render(request,TEMPLATE_ROOT+"index.html",context)


class MessageViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        message=MessageRepo(request=request).message(*args, **kwargs)
        context['message']=message
        return render(request,TEMPLATE_ROOT+"message.html",context)


class SendSMSView(View):
    def post(self,request,*args, **kwargs):
        return SendSMSApi().post(request=request)
    
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"send-sms.html",context)
    

class ChannelViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        channel=ChannelRepo(request=request).channel(*args, **kwargs)
        context['channel']=channel
        messages=MessageRepo(request=request).list(channel_id=channel.id,*args, **kwargs).order_by("-id")
        context['messages']=messages
        context.update(MemberContext(request=request))
        members=channel.member_set.all()
        context['members']=members
        context['members_s']=json.dumps(MemberSerializer(members,many=True).data)
        return render(request,TEMPLATE_ROOT+"channel.html",context)


class MemberView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        member=MemberRepo(request=request).member(*args, **kwargs)
        context['member']=member
        return render(request,TEMPLATE_ROOT+"member.html",context)


class NotificationView(View):
    def get(self,request,*args, **kwargs):
        notification=NotificationRepo(request=request).notification(*args,read=True,  **kwargs)
       
        context=getContext(request=request)
        context['notification']=notification
        notification_s=json.dumps(NotificationSerializer(notification).data)
        context['notification_s']=notification_s
        return render(request,TEMPLATE_ROOT+"notification.html",context)


class NotificationsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        notifications=NotificationRepo(request=request).notification(*args,**kwargs)
        context['notifications']=notifications
        notifications_s=json.dumps(NotificationSerializer(notifications,many=True).data)

        context['notifications_s']=notifications_s
        return render(request,TEMPLATE_ROOT+"notifications.html",context)

