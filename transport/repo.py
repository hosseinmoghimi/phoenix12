from .models import Vehicle,ServiceMan,Maintenance,OilingMaintenance,OilingMaintenanceDetail

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

        if 'hour' in kwargs:
            maintenance.hour=kwargs["hour"]
            
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


class OilingMaintenanceRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=OilingMaintenance.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_oilingmaintenance"):
                self.objects=OilingMaintenance.objects
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
        
    def oiling_maintenance(self,*args, **kwargs):
        if "oiling_maintenance_id" in kwargs and kwargs["oiling_maintenance_id"] is not None:
            return self.objects.filter(pk=kwargs['oiling_maintenance_id']).first()  
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


        if 'oiling_id' in kwargs:
            oiling_id=kwargs["oiling_id"]
            oiling=Oiling.objects.filter(pk=oiling_id).first()
            if oiling is not None:
                (result,message,invoice)=invoice.save()
                oiling.invoices.add(invoice.id)
                result=SUCCEED
                message='با موفقیت اضافه شد.'

        return result,message,invoice

     
    def add_invoice_to_oiling(self,*args, **kwargs):   
        result,message,invoice=FAILED,'',None
        if not self.request.user.has_perm(APP_NAME+".change_oiling"):
            message="دسترسی غیر مجاز"
            return result,message,invoice
        oiling=Oiling.objects.filter(pk=kwargs['oiling_id']).first()
        from accounting.repo import InvoiceRepo
        invoice=InvoiceRepo(request=self.request).invoice(pk=kwargs['invoice_id'])
        if oiling is not None and invoice is not None:
            oiling.invoices.add(invoice.id)
            result=SUCCEED
            message='با موفقیت اضافه شد.'
        return result,message,invoice
    
    def add_oiling_maintenance(self,*args,**kwargs):
        result,message,oiling_maintenance=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_oilingmaintenance"):
            message="دسترسی غیر مجاز"
            return result,message,oiling_maintenance

        oiling_maintenance=OilingMaintenance()
        if 'title' in kwargs:
            oiling_maintenance.title=kwargs["title"]
            
        if 'oil_type' in kwargs:
            oiling_maintenance.oil_type=kwargs["oil_type"]
            
        if 'oil_liter' in kwargs:
            oiling_maintenance.oil_liter=kwargs["oil_liter"]
            
        if 'fuel_liter' in kwargs:
            oiling_maintenance.fuel_liter=kwargs["fuel_liter"]
            
        if 'replace_oil' in kwargs:
            oiling_maintenance.replace_oil=kwargs["replace_oil"]
            
        if 'over_load_oil' in kwargs:
            oiling_maintenance.over_load_oil=kwargs["over_load_oil"]
            
        if 'hour' in kwargs:
            oiling_maintenance.hour=kwargs["hour"]
            
        if 'service_man_id' in kwargs:
            oiling_maintenance.service_man_id=kwargs["service_man_id"]
            
        if 'vehicle_id' in kwargs:
            oiling_maintenance.vehicle_id=kwargs["vehicle_id"]
            
        if 'kilometer' in kwargs:
            oiling_maintenance.kilometer=kwargs["kilometer"]

        if 'maintenance_type' in kwargs:
            oiling_maintenance.maintenance_type=kwargs["maintenance_type"]

        if 'description' in kwargs:
            oiling_maintenance.description=kwargs["description"]

  
            
        if 'oil_type' in kwargs:
            oiling_maintenance.oil_type=kwargs["oil_type"]
        if 'oil_liter' in kwargs:
            oiling_maintenance.oil_liter=kwargs["oil_liter"]
        if 'oil_filter' in kwargs:
            oiling_maintenance.oil_filter=kwargs["oil_filter"]
        if 'gasoil_filter' in kwargs:
            oiling_maintenance.gasoil_filter=kwargs["gasoil_filter"]
        if 'Hydrolic_filter' in kwargs:
            oiling_maintenance.Hydrolic_filter=kwargs["Hydrolic_filter"]
        if 'nano_filter' in kwargs:
            oiling_maintenance.nano_filter=kwargs["nano_filter"]
        if 'abgir_filter' in kwargs:
            oiling_maintenance.abgir_filter=kwargs["abgir_filter"]
        if 'tank_filter' in kwargs:
            oiling_maintenance.tank_filter=kwargs["tank_filter"]
        if 'bokharkesh_filter' in kwargs:
            oiling_maintenance.bokharkesh_filter=kwargs["bokharkesh_filter"]
        if 'lajangir_filter' in kwargs:
            oiling_maintenance.lajangir_filter=kwargs["lajangir_filter"]



        if 'event_datetime' in kwargs and kwargs['event_datetime'] is not None and not kwargs['event_datetime']=='':
            year=kwargs['event_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['event_datetime']=PersianCalendar().to_gregorian(kwargs["event_datetime"])
            oiling_maintenance.event_datetime=kwargs["event_datetime"]
         
        (result,message,oiling_maintenance)=oiling_maintenance.save()
        return result,message,oiling_maintenance


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
 
class OilingMaintenanceDetailRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=OilingMaintenanceDetail.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_oilingmaintenancedetail"):
                self.objects=OilingMaintenanceDetail.objects
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
        
    def oiling_maintenance_detail(self,*args, **kwargs):
        if "oiling_maintenance_detail_id" in kwargs and kwargs["oiling_maintenance_detail_id"] is not None:
            return self.objects.filter(pk=kwargs['oiling_maintenance_detail_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
    
        
    def add_oiling_maintenance_detail(self,*args,**kwargs):
        result,message,oiling_maintenance_detail=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_oilingmaintenancedetail"):
            message="دسترسی غیر مجاز"
            return result,message,oiling_maintenance_detail

        oiling_maintenance_detail=OilingMaintenanceDetail()
        if 'oiling_maintenance_id' in kwargs:
            oiling_maintenance_detail.oiling_maintenance_id=kwargs["oiling_maintenance_id"]
        if 'filter_type' in kwargs:
            oiling_maintenance_detail.filter_type=kwargs["filter_type"]
            
        if 'filter_action' in kwargs:
            oiling_maintenance_detail.filter_action=kwargs["filter_action"]
            
        if 'count' in kwargs:
            oiling_maintenance_detail.count=kwargs["count"]
            
        if 'cost' in kwargs:
            oiling_maintenance_detail.cost=kwargs["cost"]
            
        if 'description' in kwargs:
            oiling_maintenance_detail.description=kwargs["description"]
        
        (result,message,oiling_maintenance_detail)=oiling_maintenance_detail.save()
        return result,message,oiling_maintenance_detail

