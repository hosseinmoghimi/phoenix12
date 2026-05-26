from messenger.forms import *
from django.http import JsonResponse
from messenger.serializers import MessageSerializer, NotificationSerializer
from rest_framework.views import APIView
from utility.constants import FAILED,SUCCEED
from messenger.repo import MessageRepo, NotificationRepo



class SendMessageApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            send_message_form=SendMessageForm(request.POST)
            if send_message_form.is_valid():
                log=3
                message_title=send_message_form.cleaned_data['message_title']
                message_body=send_message_form.cleaned_data['message_body']
                channel_id=send_message_form.cleaned_data['channel_id']
                event=send_message_form.cleaned_data['event']
                message=MessageRepo(request=request).send_message(
                        message_title=message_title,
                        message_body=message_body,
                        channel_id=channel_id,
                        event=event)
                if message is not None:
                    context['message']=MessageSerializer(message).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    

class SendNotificationApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=1
        if request.method=='POST':
            log=2
            send_notification_form=SendNotificationForm(request.POST)
            if send_notification_form.is_valid():
                log=3
                message_title=send_notification_form.cleaned_data['message_title']
                message_body=send_notification_form.cleaned_data['message_body']
                member_id=send_notification_form.cleaned_data['member_id']
                notification=NotificationRepo(request=request).send_notification(
                        message_title=message_title,
                        message_body=message_body,
                        member_id=member_id,
                        )
                if notification is not None:
                    context['notification']=NotificationSerializer(notification).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)