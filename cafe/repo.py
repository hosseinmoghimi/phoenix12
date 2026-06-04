from .models import Table,Menu,MenuItem,TableCustomer
from .apps import APP_NAME
from .enums import *
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
from accounting.models import Account


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

  
class TableCustomerRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=TableCustomer.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_tablecustomer"):
                self.objects=TableCustomer.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def table_customer(self,*args, **kwargs):
        if "table_customer_id" in kwargs and kwargs["table_customer_id"] is not None:
            return self.objects.filter(pk=kwargs['table_customer_id']).first()  
        if "table_id" in kwargs and kwargs["table_id"] is not None:
            return self.objects.filter(table_id=kwargs['table_id']).first()  
        
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_table_customer(self,*args,**kwargs):
        result,message,table_customer=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_table_customer"):
            message="دسترسی غیر مجاز"
            return result,message,table_customer

        table_customer=TableCustomer()
        if 'title' in kwargs:
            table_customer.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                table_customer.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            table_customer.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            table_customer.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            table_customer.priority=kwargs["priority"]
        if 'type' in kwargs:
            table_customer.type=kwargs["type"]

            
        if 'parent_code' in kwargs:
            parent_code= kwargs["parent_code"]
            parent=Account.objects.filter(code=parent_code).first()
            if parent is not None:
                table_customer.parent_id=parent.id

        if 'nature' in kwargs:
            table_customer.nature=kwargs["nature"]
        (result,message,table_customer)=table_customer.save()
        return result,message,table_customer
