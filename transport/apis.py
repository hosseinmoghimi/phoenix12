
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import VehicleRepo,ServiceManRepo,MaintenanceRepo,WorkShiftRepo,AnbarProductRepo
from .serializers import MaintenanceSerializer,VehicleSerializer,ServiceManSerializer,WorkShiftSerializer,AnbarProductSerializer
from django.http import JsonResponse
from .forms import *
from accounting.serializers import InvoiceSerializer

class AddOilingMaintenanceDetailApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_oiling_maintenance_detail_form=AddOilingMaintenanceDetailForm(request.POST)
        if add_oiling_maintenance_detail_form.is_valid():
            log=333
            cd=add_oiling_maintenance_detail_form.cleaned_data
            result,message,oiling_maintenance_detail=OilingMaintenanceDetailRepo(request=request).add_oiling_maintenance_detail(**cd)
            if oiling_maintenance_detail is not None:
                context['oiling_maintenance_detail']=OilingMaintenanceDetailSerializer(oiling_maintenance_detail).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)



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




class ImportVehicleFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        import_vehicles_form=ImportVehicleFromExcelForm(request.POST,request.FILES)
        if import_vehicles_form.is_valid():
            log=333
            cd=import_vehicles_form.cleaned_data
            
            excel_file = request.FILES['file1']
            cd['excel_file']=excel_file
            result,message,vehicles=VehicleRepo(request=request).import_vehicles_from_excel(**cd)
            if vehicles is not None:
                context['vehicles']=VehicleSerializer(vehicles,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)





class GetReportApiw(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        get_report_form=GetReportForm(request.POST)
        if get_report_form.is_valid():
            log=333
            cd=get_report_form.cleaned_data
            
            work_shifts=WorkShiftRepo(request=request).list(**cd)
            context['work_shifts']=WorkShiftSerializer(work_shifts,many=True).data

            
            
            anbar_products=AnbarProductRepo(request=request).list(**cd)
            context['anbar_products']=AnbarProductSerializer(anbar_products,many=True).data
            
            message+="گزارش گیری انجام شد."

            if "from_shift_date" in cd and cd['from_shift_date']:
                from_shift_date=PersianCalendar().to_gregorian(cd["from_shift_date"])
                from_shift_date=PersianCalendar().from_gregorian(from_shift_date)
                import datetime 
                # from_shift_date=datetime(from_shift_date)
                message+="از تاریخ "+str(from_shift_date)


            if "to_shift_date" in cd and cd['to_shift_date']:
                to_shift_date=PersianCalendar().to_gregorian(cd["to_shift_date"])
                 
                # to_shift_date=datetime(to_shift_date)
                delta=datetime.timedelta(hours=23,minutes=59,seconds=59)
                to_shift_date=to_shift_date+delta
                
                print(to_shift_date) 
                to_shift_date=PersianCalendar().from_gregorian(to_shift_date)

                print(to_shift_date)
                message+="تا تاریخ "+str(to_shift_date)


            result=SUCCEED
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)



class AddWorkShiftApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_work_shift_form=AddWorkShiftForm(request.POST)
        if add_work_shift_form.is_valid():
            log=333
            cd=add_work_shift_form.cleaned_data
            cd['filters']=json.loads(cd['filters'])
            cd['oils']=json.loads(cd['oils'])
            cd['tavaghofs']=json.loads(cd['tavaghofs'])
            cd['products']=json.loads(cd['products'])
            result,message,work_shift=WorkShiftRepo(request=request).add_work_shift(**cd)
            if work_shift is not None:
                context['work_shift']=WorkShiftSerializer(work_shift).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)



class AddKarkerdApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_karkerd_form=AddKarkerdForm(request.POST)
        if add_karkerd_form.is_valid():
            log=333
            cd=add_karkerd_form.cleaned_data
            
            result,message,karkerd=KarkerdRepo(request=request).add_karkerd(**cd)
            if karkerd is not None:
                context['karkerd']=KarkerdSerializer(karkerd).data
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
         
    

class AddOilingMaintenanceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_oiling_maintenance_form=AddOilingMaintenanceForm(request.POST)
        if add_oiling_maintenance_form.is_valid():
            log=333
            cd=add_oiling_maintenance_form.cleaned_data
            result,message,oiling_maintenance=OilingMaintenanceRepo(request=request).add_oiling_maintenance(**cd)
            if oiling_maintenance is not None:
                context['oiling_maintenance']=OilingMaintenanceSerializer(oiling_maintenance).data
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
  
 