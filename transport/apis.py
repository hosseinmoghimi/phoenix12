
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import VehicleRepo,ServiceManRepo,MaintenanceRepo
from .serializers import MaintenanceSerializer,VehicleSerializer,ServiceManSerializer
from django.http import JsonResponse
from .forms import *
from accounting.serializers import InvoiceSerializer


class AddVehicleApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_vehicle_form=AddVehicleForm(request.POST)
        if add_vehicle_form.is_valid():
            log=333
            cd=add_vehicle_form.cleaned_data
            result,message,vehicle=VehicleRepo(request=request).add_vehicle(**cd)
            if vehicle is not None:
                context['vehicle']=VehicleSerializer(vehicle).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddInvoiceToMaintenanceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_invoice_to_maintenance_form=AddInvoiceToMaintenanceForm(request.POST)
        if add_invoice_to_maintenance_form.is_valid():
            log=333
            cd=add_invoice_to_maintenance_form.cleaned_data
            result,message,invoice=MaintenanceRepo(request=request).add_invoice_to_maintenance(**cd)
            if invoice is not None:
                context['invoice']=InvoiceSerializer(invoice).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
 
class AddInvoiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_maintenance_invoice_form=AddInvoiceForm(request.POST)
        if add_maintenance_invoice_form.is_valid():
            log=333
            cd=add_maintenance_invoice_form.cleaned_data
            result,message,invoice=MaintenanceRepo(request=request).add_invoice(**cd)
            if invoice is not None:
                context['invoice']=InvoiceSerializer(invoice).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    

class AddMaintenanceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_maintenance_form=AddMaintenanceForm(request.POST)
        if add_maintenance_form.is_valid():
            log=333
            cd=add_maintenance_form.cleaned_data
            result,message,maintenance=MaintenanceRepo(request=request).add_maintenance(**cd)
            if maintenance is not None:
                context['maintenance']=MaintenanceSerializer(maintenance).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    

class AddServiceManApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_service_man_form=AddServiceManForm(request.POST)
        if add_service_man_form.is_valid():
            log=333
            cd=add_service_man_form.cleaned_data
            result,message,service_man=ServiceManRepo(request=request).add_service_man(**cd)
            if service_man is not None:
                context['service_man']=ServiceManSerializer(service_man).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
 