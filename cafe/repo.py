from .models import Table,Menu,Order,OrderLog
from .apps import APP_NAME
from .enums import *
import json
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import * 
from market.repo import CustomerRepo,SupplierRepo,ShopRepo


class MenuRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Menu.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Menu.objects
            if request.user.has_perm(APP_NAME+".view_menu"):
                self.objects=Menu.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def menu(self,*args, **kwargs):
        if "menu_id" in kwargs and kwargs["menu_id"] is not None:
            return self.objects.filter(pk=kwargs['menu_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_menu(self,*args,**kwargs):
        result,message,menu=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_menu"):
            message="دسترسی غیر مجاز"
            return result,message,menu

        menu=Menu()
        if 'title' in kwargs:
            menu.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                menu.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            menu.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            menu.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            menu.priority=kwargs["priority"]
        if 'type' in kwargs:
            menu.type=kwargs["type"]

            
        

        if 'nature' in kwargs:
            menu.nature=kwargs["nature"]
        (result,message,menu)=menu.save()
        return result,message,menu


class TableRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Table.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=Table.objects
                self.my_accounts=self.objects 
    
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "status" in kwargs:
            status=kwargs["status"]
            orders=Order.objects.filter(status=status)
            
            tables=[]
            for order in orders:
                tables.append(order.table_id)
            return Table.objects.filter(id__in=tables)


        return objects.all()
        
    def table(self,*args, **kwargs):
        if "table_id" in kwargs and kwargs["table_id"] is not None:
            return self.objects.filter(pk=kwargs['table_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first()  
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_table(self,*args,**kwargs):
        result,message,table=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_table"):
            message="دسترسی غیر مجاز"
            return result,message,table

        table=Table()
        if 'title' in kwargs:
            table.title=kwargs["title"]
        if 'supplier_id' in kwargs:
            table.supplier_id=kwargs["supplier_id"]
        if 'code' in kwargs:
            table.code=kwargs["code"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                table.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            table.color=kwargs["color"]
        if 'code' in kwargs:
            table.code=kwargs["code"]
        if 'priority' in kwargs:
            table.priority=kwargs["priority"]
        if 'table_no' in kwargs:
            table.table_no=kwargs["table_no"]
 

        if 'nature' in kwargs:
            table.nature=kwargs["nature"]
        table.save()
        if table.id is not None and table.id>0:
            message='با موفقیت ذخیره شد.'
            result=SUCCEED
            return result,message,table
        else:
            return result,message,None

   
def checkout_cart(request,*args, **kwargs):
    result,message,invoices=FAILED,'',[]

    
    if request.user.has_perm(APP_NAME+".add_cartitem"):
            pass
            
    else :
        me_customer=CustomerRepo(request=request).me
        if me_customer is None:
            
            message="دسترسی غیر مجاز"
            return result,message,invoices
        elif customer_id==me_customer.id:
            pass
        else:
            message="دسترسی غیر مجاز"
            return result,message,invoices
                 
    table_id=int(kwargs['table_id'])
    table=TableRepo(request=request).table(pk=table_id)
    customer_repo=CustomerRepo(request=request)   
    customer=None
    if "customer_id" in kwargs and kwargs['customer_id']:
        
        customer_id=int(kwargs['customer_id'])
        customer=customer_repo.customer(pk=customer_id) 

    if customer is None:
        customer=customer_repo.misc_customer()  
    cart_items=json.loads(kwargs['cart_items'])
    description=kwargs['description']
    if len(cart_items)<1:
        message='سبد خرید خالی است'
        return result,message,invoice
    

    shop_repo=ShopRepo(request=request)
    supplier_repo=SupplierRepo(request=request)

    suppliers_ids=[] 
    for cart_item in cart_items:
        shop=shop_repo.shop(pk=cart_item['shop_id'])
        if shop is not None:
            supplier_id=shop.supplier.id
            if supplier_id not in suppliers_ids:
                suppliers_ids.append(supplier_id)

      
    for supplier_id in suppliers_ids:
        supplier=supplier_repo.supplier(pk=supplier_id)
        from django.utils import timezone
        invoice_data={}
        title=" خرید از "+supplier.title+" "+table.title
        if 'title' in kwargs and kwargs['title']:
            title=kwargs['title']
        invoice_data['title']=title
        invoice_data['bedehkar_id']=customer.person_account.id
        invoice_data['bestankar_id']=supplier.person_account.id
        invoice_data['amount']=0
        invoice_data['description']="میز : "+table.title+'<br>'+description
         
        invoice_data['event_datetime']=timezone.now()
        from accounting.models import Invoice,InvoiceLine
        invoice=Invoice(**invoice_data)
        invoice.save()


        log_data={}
        from log.repo import LogRepo
        log_data['person_id']=PersonRepo(request=request).me.id
        log_data['url']=invoice.get_absolute_url()
        log_data['title']="ذخیره فاکتور جدید"
        log_data['description']="فاکتور جدید"
        log_data['app_name']=APP_NAME
        LogRepo(request=request).add_log(**log_data)




        invoices.append(invoice)
        for cart_item in cart_items:
            shop=shop_repo.shop(shop_id=cart_item['shop_id'])
            if shop.supplier.id==supplier_id:
                if cart_item['quantity']>shop.available:
                    message="تعداد درخواستی از موجودی بیشتر است."
                    return FAILED,message,None
                invoice_line=InvoiceLine()
                invoice_line.discount_percentage=shop.discount_percentage
                invoice_line.invoice_id=invoice.id
                invoice_line.invoice_line_item_id=shop.product_id
                invoice_line.quantity=cart_item['quantity'] 
                if not invoice_line.quantity>shop.available:
                    invoice_line.unit_price=shop.unit_price
                    invoice_line.unit_name=shop.unit_name
                    invoice_line.save() 
                    shop.available-=cart_item['quantity']
                    shop.save()
        result=SUCCEED
        message='با موفقیت ذخیره شد'
   
    return result,message,invoices