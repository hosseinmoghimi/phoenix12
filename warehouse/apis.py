
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import WareHouseRepo,WareHouseSheetRepo,WareHouseSheetSignatureRepo,WareHouseSheetLabelRepo,ProductInWareHouseRepo
from .serializers import ProductInWareHouseSerializer,WareHouseSerializer,WareHouseSheetSerializer,WareHouseSheetSignatureSerializer,WareHouseSheetLabelSerializer
 
from django.http import JsonResponse
from .forms import *
   
class SelectWareHouseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        select_warehouse_form=SelectWareHouseForm(request.POST)
        if select_warehouse_form.is_valid():
            log=333
            cd=select_warehouse_form.cleaned_data
            warehouse_id=cd['warehouse_id']
            warehouse=WareHouseRepo(request=request).warehouse(warehouse_id=warehouse_id)
            message='انبار پیدا نشد.'
            if warehouse is not None:
                context['warehouse']=WareHouseSerializer(warehouse).data
                result=SUCCEED
                message='انبار پیدا شد.'
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   
 
class AddWareHouseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_warehouse_form=AddWareHouseForm(request.POST)
        if add_warehouse_form.is_valid():
            log=333
            cd=add_warehouse_form.cleaned_data
            result,message,warehouse=WareHouseRepo(request=request).add_warehouse(**cd)
            if warehouse is not None:
                context['warehouse']=WareHouseSerializer(warehouse).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    

class NormalizeProductInWareHouseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        normalize_product_in_warehouse_form=NormalizeProductInWareHouseForm(request.POST)
        if normalize_product_in_warehouse_form.is_valid():
            log=333
            cd=normalize_product_in_warehouse_form.cleaned_data
            result,message,warehouse=ProductInWareHouseRepo(request=request).normalize_product_in_warehouse(**cd)
            if warehouse is not None:
                context['product_in_warehouse']=WareHouseSerializer(warehouse).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
    

class AddMaterialRequestApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_material_request_form=AddMaterialRequestForm(request.POST)
        if add_material_request_form.is_valid():
            log=333
            cd=add_material_request_form.cleaned_data
            result,message,warehouse_sheet,invoice_line=WareHouseSheetRepo(request=request).add_material_request(**cd)
            if warehouse_sheet is not None:
                context['warehouse_sheet']=WareHouseSheetSerializer(warehouse_sheet).data
            if invoice_line is not None:
                from accounting.apis import InvoiceLineSerializer
                context['invoice_line']=InvoiceLineSerializer(invoice_line).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
class AddInvoiceWareHouseSheetsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_invoice_warehouse_sheets_form=AddInvoiceWareHouseSheetsForm(request.POST)
        if add_invoice_warehouse_sheets_form.is_valid():
            log=333
            cd=add_invoice_warehouse_sheets_form.cleaned_data
            result,message,warehouse_sheets=WareHouseSheetRepo(request=request).add_invoice_warehouse_sheets(**cd)
            if warehouse_sheets is not None and len(warehouse_sheets)>0:
                context['warehouse_sheets']=WareHouseSheetSerializer(warehouse_sheets,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
      
    
class AddWareHouseSheetApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_warehouse_sheet_form=AddWareHouseSheetForm(request.POST)
        if add_warehouse_sheet_form.is_valid():
            log=333
            cd=add_warehouse_sheet_form.cleaned_data
            result,message,warehouse_sheet=WareHouseSheetRepo(request=request).add_warehouse_sheet(**cd)
            if warehouse_sheet is not None:
                context['warehouse_sheet']=WareHouseSheetSerializer(warehouse_sheet).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   



class ProductInWareHouseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        product_in_warehouse_form=ProductInWareHouseForm(request.POST)
        if product_in_warehouse_form.is_valid():
            log=333
            cd=product_in_warehouse_form.cleaned_data
            product_in_warehouses=ProductInWareHouseRepo(request=request).list(**cd)
            # product_in_warehouses=ProductInWareHouseRepo(request=request).list()
            if True or product_in_warehouses:
                context['product_in_warehouses']=ProductInWareHouseSerializer(product_in_warehouses,many=True).data
                message='موجودی انبار گرفته شد.'
                result=SUCCEED
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   

class AddWareHouseSheetSignatureApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_warehouse_sheet_signature_form=AddWareHouseSheetSignatureForm(request.POST)
        if add_warehouse_sheet_signature_form.is_valid():
            log=333
            cd=add_warehouse_sheet_signature_form.cleaned_data
            result,message,warehouse_sheet_signature=WareHouseSheetSignatureRepo(request=request).add_warehouse_sheet_signature(**cd)
            if warehouse_sheet_signature is not None:
                context['warehouse_sheet_signature']=WareHouseSheetSignatureSerializer(warehouse_sheet_signature).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   
 
class AddWareHouseSheetLabelApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_warehouse_sheet_label_form=AddWareHouseSheetLabelForm(request.POST)
        if add_warehouse_sheet_label_form.is_valid():
            log=333
            cd=add_warehouse_sheet_label_form.cleaned_data
            result,message,warehouse_sheet_label=WareHouseSheetLabelRepo(request=request).add_warehouse_sheet_label(**cd)
            if warehouse_sheet_label is not None:
                context['warehouse_sheet_label']=WareHouseSheetLabelSerializer(warehouse_sheet_label).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   