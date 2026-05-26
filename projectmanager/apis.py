
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import ProjectRepo,RemoteClientRepo,TicketRepo
from core.serializers import EventSerializer
from .serializers import ProjectSerializer,RemoteClientSerializer,TicketSerializer
from accounting.serializers import InvoiceSerializer
from django.http import JsonResponse
from .forms import *
   

   

class SelectProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        select_project_form=SelectProjectForm(request.POST)
        if select_project_form.is_valid():
            log=333
            cd=select_project_form.cleaned_data
            project=ProjectRepo(request=request).project(**cd)
            if project is not None:
                context['project']=ProjectSerializer(project).data
                result=SUCCEED
                message='موفق'
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 


class AddTicketApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_ticket_form=AddTicketForm(request.POST)
        if add_ticket_form.is_valid():
            log=333
            cd=add_ticket_form.cleaned_data
            result,message,ticket=TicketRepo(request=request).add_ticket(**cd)
            if ticket is not None:
                context['ticket']=TicketSerializer(ticket).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

   
class AddProjectInvoiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_invoice_form=AddProjectInvoiceForm(request.POST)
        if add_invoice_form.is_valid():
            log=333
            cd=add_invoice_form.cleaned_data
            result,message,invoice=ProjectRepo(request=request).add_invoice(**cd)
            if invoice is not None:
                context['invoice']=InvoiceSerializer(invoice).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class EditProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        if request.method=='POST':
            log=2
            edit_project_form=EditProjectForm(request.POST)
            if edit_project_form.is_valid():
                cd=edit_project_form.cleaned_data 
                
                cd['start_datetime']=PersianCalendar().to_gregorian(cd['start_datetime'])
                cd['end_datetime']=PersianCalendar().to_gregorian(cd['end_datetime'])
                project=ProjectRepo(request=request).edit_project(**cd)
                if project is not None: 
                    context['project']=ProjectSerializer(project).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
 
 
class NormalizeProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log=2
            result=FAILED
            message=""
            normalize_project_form=NormalizeProjectForm(request.POST)
            if normalize_project_form.is_valid():
                cd=normalize_project_form.cleaned_data 
              
                result,message,project=ProjectRepo(request=request).normalize_project(**cd)
                if project is not None: 
                    context['project']=ProjectSerializer(project).data
        context['result']=result
        context['message']=message
        context['log']=log
        return JsonResponse(context)
 
 
class AddRemoteClientApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        context['result']=FAILED
        message=""
        result=FAILED
        log=2
        AddRemoteClientForm_=AddRemoteClientForm(request.POST)
        is_valid=AddRemoteClientForm_.is_valid()
        if not is_valid:
            message='داده های فرم مجاز نیستند.'
        if is_valid:
            log=3  
            cd=AddRemoteClientForm_.cleaned_data
            result,message,remote_client=RemoteClientRepo(request=request).add_remote_client(**cd)
            if remote_client is not None:
                context['remote_client']=RemoteClientSerializer(remote_client).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
 
class AddProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_project_form=AddProjectForm(request.POST)
        if add_project_form.is_valid():
            log=333
            cd=add_project_form.cleaned_data
            result,message,project=ProjectRepo(request=request).add_project(**cd)
            if project is not None:
                context['project']=ProjectSerializer(project).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class AddSubProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_sub_project_form=AddSubProjectForm(request.POST)
        if add_sub_project_form.is_valid():
            log=333
            cd=add_sub_project_form.cleaned_data
            result,message,project=ProjectRepo(request=request).add_project(**cd)
            if project is not None:
                context['project']=ProjectSerializer(project).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
 
class AddInvoiceToProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_invoice_to_project_form=AddInvoiceToProjectForm(request.POST)
        if add_invoice_to_project_form.is_valid():
            log=333
            cd=add_invoice_to_project_form.cleaned_data
            result,message,invoice=ProjectRepo(request=request).add_invoice_to_project(**cd)
            if result==SUCCEED:
                context['invoice']=InvoiceSerializer(invoice).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class AddEventToProjectApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_evet_to_project_form=AddEventToProjectForm(request.POST)
        if add_evet_to_project_form.is_valid():
            log=333
            cd=add_evet_to_project_form.cleaned_data
            cd['start_datetime']=PersianCalendar().to_gregorian(cd['start_datetime'])
            cd['end_datetime']=PersianCalendar().to_gregorian(cd['end_datetime'])
            cd['event_datetime']=PersianCalendar().to_gregorian(cd['event_datetime'])
                
            result,message,events=ProjectRepo(request=request).add_event_to_project(**cd)
            if result==SUCCEED:
                context['events']=EventSerializer(events,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 