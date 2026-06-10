from .models import Vehicle,ServiceMan,Maintenance

from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from utility.calendar import PersianCalendar

class VehicleRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Vehicle.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=Vehicle.objects
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
        
    def vehicle(self,*args, **kwargs):
        if "vehicle_id" in kwargs and kwargs["vehicle_id"] is not None:
            return self.objects.filter(pk=kwargs['vehicle_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_vehicle(self,*args,**kwargs):
        result,message,vehicle=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_vehicle"):
            message="دسترسی غیر مجاز"
            return result,message,vehicle

        vehicle=Vehicle()
        if 'title' in kwargs:
            vehicle.title=kwargs["title"]
            if len(Vehicle.objects.filter(title=vehicle.title))>0:
                message='نام تکراری برای وسیله نقلیه جدید'
                return FAILED,message,None
        if 'owner_id' in kwargs:
            vehicle.owner_id=kwargs["owner_id"]
          
        (result,message,vehicle)=vehicle.save()
        return result,message,vehicle


  

class MaintenanceRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Maintenance.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_maintenance"):
                self.objects=Maintenance.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "vehicle_id" in kwargs:
            vehicle_id=kwargs["vehicle_id"]
            objects=objects.filter(vehicle_id=vehicle_id)  
        if "service_man_id" in kwargs:
            service_man_id=kwargs["service_man_id"]
            objects=objects.filter(service_man_id=service_man_id)
        return objects.all()
        
    def maintenance(self,*args, **kwargs):
        if "maintenance_id" in kwargs and kwargs["maintenance_id"] is not None:
            return self.objects.filter(pk=kwargs['maintenance_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
    
       

    def add_invoice(self,*args,**kwargs):
        result,message,invoice=FAILED,"",None 
        from accounting.models import Invoice,PersianCalendar

            
        if not self.request.user.has_perm(APP_NAME+".add_invoice"):
            message="دسترسی غیر مجاز"
            return result,message,invoice

        invoice=Invoice()
        
        if 'valid' in kwargs and kwargs['valid'] is not None:
            invoice.valid=kwargs["valid"]

        if 'title' in kwargs:
            invoice.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                invoice.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            invoice.color=kwargs["color"]
        if 'code' in kwargs:
            invoice.code=kwargs["code"]
        if 'priority' in kwargs:
            invoice.priority=kwargs["priority"]
        if 'bedehkar_id' in kwargs:
            invoice.bedehkar_id=kwargs["bedehkar_id"]
        if 'bestankar_id' in kwargs:
            invoice.bestankar_id=kwargs["bestankar_id"]
        if 'event_datetime' in kwargs:
            
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            invoice.event_datetime=kwargs["event_datetime"]

        if 'type' in kwargs:
            invoice.type=kwargs["type"]

           
        if 'status' in kwargs:
            invoice.status=kwargs["status"]

           
           
        if 'invoice_no' in kwargs:
            invoice.invoice_no=kwargs["invoice_no"]


        if 'maintenance_id' in kwargs:
            maintenance_id=kwargs["maintenance_id"]
            maintenance=Maintenance.objects.filter(pk=maintenance_id).first()
            if maintenance is not None:
                (result,message,invoice)=invoice.save()
                maintenance.invoices.add(invoice.id)
                result=SUCCEED
                message='با موفقیت اضافه شد.'

        return result,message,invoice

     
    def add_invoice_to_maintenance(self,*args, **kwargs):   
        result,message,invoice=FAILED,'',None
        if not self.request.user.has_perm(APP_NAME+".change_maintenance"):
            message="دسترسی غیر مجاز"
            return result,message,invoice
        maintenance=Maintenance.objects.filter(pk=kwargs['maintenance_id']).first()
        from accounting.repo import InvoiceRepo
        invoice=InvoiceRepo(request=self.request).invoice(pk=kwargs['invoice_id'])
        if maintenance is not None and invoice is not None:
            maintenance.invoices.add(invoice.id)
            result=SUCCEED
            message='با موفقیت اضافه شد.'
        return result,message,invoice
    
    def add_maintenance(self,*args,**kwargs):
        result,message,maintenance=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_maintenance"):
            message="دسترسی غیر مجاز"
            return result,message,maintenance

        maintenance=Maintenance()
        if 'title' in kwargs:
            maintenance.title=kwargs["title"]
            
        if 'service_man_id' in kwargs:
            maintenance.service_man_id=kwargs["service_man_id"]
            
        if 'vehicle_id' in kwargs:
            maintenance.vehicle_id=kwargs["vehicle_id"]
            
        if 'kilometer' in kwargs:
            maintenance.kilometer=kwargs["kilometer"]

        if 'maintenance_type' in kwargs:
            maintenance.maintenance_type=kwargs["maintenance_type"]

        if 'description' in kwargs:
            maintenance.description=kwargs["description"]


        if 'event_datetime' in kwargs and kwargs['event_datetime'] is not None and not kwargs['event_datetime']=='':
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            maintenance.event_datetime=kwargs["event_datetime"]
         
        (result,message,maintenance)=maintenance.save()
        return result,message,maintenance


class ServiceManRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=ServiceMan.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=ServiceMan.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(person_account__person__full_name__contains=search_for)    )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def service_man(self,*args, **kwargs):
        if "service_man_id" in kwargs and kwargs["service_man_id"] is not None:
            return self.objects.filter(pk=kwargs['service_man_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_service_man(self,*args,**kwargs):
        result,message,service_man=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_service_man"):
            message="دسترسی غیر مجاز"
            return result,message,service_man
        if len(ServiceMan.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='قبلا برای این شخص سرویس کار ایجاد شده است.'
            return FAILED,message,None
        service_man=ServiceMan() 
        if 'person_account_id' in kwargs:
            service_man.person_account_id=kwargs["person_account_id"]
          
        (result,message,service_man)=service_man.save()
        return result,message,service_man
 