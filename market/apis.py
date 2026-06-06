
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import ShopRepo,SupplierRepo,CustomerRepo,ShipperRepo,CartItemRepo
from accounting.apis import InvoiceRepo,InvoiceSerializer
from .serializers import ShopSerializer,CartItemSerializer,SupplierSerializer,CustomerSerializer,ShipperSerializer
from django.http import JsonResponse
from .enums import *
from .forms import *
   

  
class AddShopPackageApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_menu_form=AddMenuForm(request.POST)
        if add_menu_form.is_valid():
            log=333
            cd=add_menu_form.cleaned_data
            result,message,menu=MenuRepo(request=request).add_menu(**cd)
            if menu is not None:
                context['menu']=MenuSerializer(menu).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
 

class ImportShopsFromExcelApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        
        message_shops=''
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            import_from_excel_form=ImportShopFromExcelForm(request.POST,request.FILES)
            if import_from_excel_form.is_valid():
                log=333
                
                excel_file = request.FILES['file1']
                cd=import_from_excel_form.cleaned_data
                cd['excel_file']=excel_file
                result,message_shops,shops=ShopRepo(request=request).import_shops_from_excel(**cd)
                if shops is not None:
                    context['shops']=ShopSerializer(shops,many=True).data
                 
        context['message_shops']=message_shops
        context['result']=result
        context['log']=log
        return JsonResponse(context)



  
class AddCartItemApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_to_cart_form=AddCartItemForm(request.POST)
        if add_to_cart_form.is_valid():
            log=333
            cd=add_to_cart_form.cleaned_data
            result,message,cart_item,cart_items=CartItemRepo(request=request).add_cart_item(**cd)
            if result==SUCCEED:
                context['cart_item']=CartItemSerializer(cart_item).data
                context['cart_items']=CartItemSerializer(cart_items,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
  
class ChangeCartItemApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_to_cart_form=ChangeCartItemForm(request.POST)
        if add_to_cart_form.is_valid():
            log=333
            cd=add_to_cart_form.cleaned_data
            result,message,cart_item,cart_items=CartItemRepo(request=request).change_cart_item(**cd)
            if result==SUCCEED:
                context['cart_item']=CartItemSerializer(cart_item).data
                context['cart_items']=CartItemSerializer(cart_items,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddShopApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_shop_form=AddShopForm(request.POST)
        if add_shop_form.is_valid():
            log=333
            cd=add_shop_form.cleaned_data
            result,message,shop=ShopRepo(request=request).add_shop(**cd)
            if shop is not None:
                context['shop']=ShopSerializer(shop).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  

class CheckoutCartApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        checkout_cart_form=CheckoutCartForm(request.POST)
        if checkout_cart_form.is_valid():
            log=333
            cd=checkout_cart_form.cleaned_data
            cd['cart_items']=json.loads(cd['cart_items'])
            result,message,invoices=CartItemRepo(request=request).checkout(**cd)
            
            if result == SUCCEED:
                context['invoices']=InvoiceSerializer(invoices,many=True).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
  
class AddCustomerApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_customer_form=AddCustomerForm(request.POST)
            if add_customer_form.is_valid():
                log=333
                cd=add_customer_form.cleaned_data
                cd['groups_ids']=json.loads(cd['groups_ids'])
                result,message,customer=CustomerRepo(request=request).add_customer(**cd)
                if result==SUCCEED:
                    context['customer']=CustomerSerializer(customer).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddSupplierApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_supplier_form=AddSupplierForm(request.POST)            
            if add_supplier_form.is_valid():
                log=333
                cd=add_supplier_form.cleaned_data
                result,message,supplier=SupplierRepo(request=request).add_supplier(**cd)
                if result==SUCCEED:
                    context['supplier']=SupplierSerializer(supplier).data
            else:    
                add_supplier_form=AddSupplierByPersonForm(request.POST)
                if add_supplier_form.is_valid():
                    log=333
                    cd=add_supplier_form.cleaned_data
                    result,message,supplier=SupplierRepo(request=request).add_supplier(**cd)
                    if result==SUCCEED:
                        context['supplier']=SupplierSerializer(supplier).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


class AddShipperApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            add_shipper_form=AddShipperForm(request.POST)            
            if add_shipper_form.is_valid():
                log=333
                cd=add_shipper_form.cleaned_data
                result,message,shipper=ShipperRepo(request=request).add_shipper(**cd)
                if result==SUCCEED:
                    context['shipper']=ShipperSerializer(shipper).data
            
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

