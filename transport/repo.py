from .models import Vehicle,ServiceMan,Maintenance,VehicleStatus,WorkShift,Driver
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from utility.calendar import PersianCalendar
from .models import VehicleEvent,Tavaghof,VehicleStatus
from .models import FilterService,OilService,Tavaghof,Product,AnbarProduct,Service

class VehicleStatusRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=VehicleStatus.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=VehicleStatus.objects
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
        return objects.all()
        
    def vehicle_status(self,*args, **kwargs):
        if "vehicle_status_id" in kwargs and kwargs["vehicle_status_id"] is not None:
            return self.objects.filter(pk=kwargs['vehicle_status_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_vehicle_status(self,*args,**kwargs):
        result,message,vehicle_status=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_vehicle"):
            message="دسترسی غیر مجاز"
            return result,message,vehicle_status

        vehicle_status=VehicleStatus()
        if 'title' in kwargs:
            vehicle_status.title=kwargs["title"]
            if len(Vehicle.objects.filter(title=vehicle_status.title))>0:
                message='نام تکراری برای وسیله نقلیه جدید'
                return FAILED,message,None
        if 'owner_id' in kwargs:
            vehicle_status.owner_id=kwargs["owner_id"]
        if 'brand_name' in kwargs:
            vehicle_status.brand_name=kwargs["brand_name"]
        if 'model_name' in kwargs:
            vehicle_status.model_name=kwargs["model_name"]
        if 'plaque' in kwargs:
            vehicle_status.plaque=kwargs["plaque"]
        if 'year' in kwargs:
            vehicle_status.year=kwargs["year"]
        if 'kilometer' in kwargs:
            vehicle_status.kilometer=kwargs["kilometer"]
        if 'driver_id' in kwargs:
            driver_id=kwargs["driver_id"]
            if driver_id is not None and driver_id>0:
                driver=DriverRepo(request=self.request).driver(driver_id=driver_id)
                if driver is not None:
                    vehicle_status.driver=driver.person_account.person.full_name
          
        if 'price' in kwargs:
            vehicle_status.price=kwargs["price"]
        
        (result,message,vehicle_status)=vehicle_status.save()
        return result,message,vehicle_status

    def last_statuses(self,*args, **kwargs):
        return self.list(*args, **kwargs)

 
class WorkShiftRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=WorkShift.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=WorkShift.objects
                self.my_accounts=self.objects 

    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
         
        if "shift" in kwargs and kwargs["shift"]:
            objects=objects.filter(shift=kwargs["shift"])

        if "location" in kwargs and kwargs["location"]:
            objects=objects.filter(location=kwargs["location"]) 
        if "vehicle_id" in kwargs:
            vehicle_id=kwargs["vehicle_id"]
            objects=objects.filter(vehicle_id=vehicle_id)  

        if "vehicle_code" in kwargs and kwargs['vehicle_code']:
            objects=objects.filter(vehicle__vehicle_code=kwargs["vehicle_code"])  
        if "driver_id" in kwargs and kwargs["driver_id"]:
            objects=objects.filter(driver_id=kwargs["driver_id"])  
        if "shift_date" in kwargs:
            year=kwargs['shift_date'][:2]
            if year=="13" or year=="14":
                kwargs['shift_date']=PersianCalendar().to_gregorian(kwargs["shift_date"])
                kwargs['shift_date']=kwargs['shift_date'].date()
            objects=objects.filter(shift_date=kwargs["shift_date"]) 

            
        if "shift" in kwargs and kwargs['shift']:
            objects=objects.filter(shift=kwargs["shift"])  
        return objects.all()
        
    def work_shift(self,*args, **kwargs):
        if "work_shift_id" in kwargs and kwargs["work_shift_id"] is not None:
            return self.objects.filter(pk=kwargs['work_shift_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_work_shift(self,*args,**kwargs):

        result,message,work_shift=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_vehicle"):
            message="دسترسی غیر مجاز"
            return result,message,work_shift

        work_shift=WorkShift()
        if 'title' in kwargs:
            work_shift.title=kwargs["title"]
            if len(Vehicle.objects.filter(title=work_shift.title))>0:
                message='نام تکراری برای وسیله نقلیه جدید'
                return FAILED,message,None
        if 'vehicle_code' in kwargs:
            vehicle_code=kwargs["vehicle_code"]
            vehicle=Vehicle.objects.filter(vehicle_code=vehicle_code).first()
            if vehicle is not None:
                work_shift.vehicle=vehicle

        if 'driver_id' in kwargs:
            work_shift.driver_id=kwargs["driver_id"]

        if 'location' in kwargs:
            work_shift.location=kwargs["location"]

        if 'shift_date' in kwargs:
            year=kwargs['shift_date'][:2]
            if year=="13" or year=="14":
                kwargs['shift_date']=PersianCalendar().to_gregorian(kwargs["shift_date"])
            work_shift.shift_date=kwargs["shift_date"]

        if 'shift' in kwargs:
            work_shift.shift=kwargs["shift"]
        if 'start_hour' in kwargs:
            work_shift.start_hour=kwargs["start_hour"]
        if 'end_hour' in kwargs:
            work_shift.end_hour=kwargs["end_hour"]

        if 'vehicle_start_hour' in kwargs:
                    work_shift.vehicle_start_hour=kwargs["vehicle_start_hour"]

        if 'vehicle_end_hour' in kwargs:
                    work_shift.vehicle_end_hour=kwargs["vehicle_end_hour"]


        if 'service_count' in kwargs:
            work_shift.service_count=kwargs["service_count"]

        if 'bar' in kwargs:
            work_shift.bar=kwargs["bar"]

        if 'description' in kwargs:
            work_shift.description=kwargs["description"]
 
 
        if 'gasoil_liter' in kwargs:
            work_shift.gasoil_liter=kwargs["gasoil_liter"]
          
         

        
        (result,message,work_shift)=work_shift.save()

        if 'filters' in kwargs and result==SUCCEED:
            filters=kwargs["filters"] 
            for filter_ in filters:
                filter_service=FilterService()
                filter_service.filter_type=filter_['filter_type']
                filter_service.filter_action=filter_['filter_action']
                filter_service.count=filter_['count']
                filter_service.cost=filter_['cost']
                filter_service.description=filter_['description']
                filter_service.work_shift=work_shift
                filter_service.save()

                
        if 'oils' in kwargs and result==SUCCEED:
            oils=kwargs["oils"] 
            for oil_ in oils:
                oil_service=OilService()
                oil_service.oil_type=oil_['oil_type']
                oil_service.oil_action=oil_['oil_action']
                oil_service.oil_liter=oil_['oil_liter']
                oil_service.cost=oil_['cost']
                oil_service.description=oil_['description']
                oil_service.work_shift=work_shift
                oil_service.save()

                
        if 'tavaghofs' in kwargs and result==SUCCEED:
            tavaghofs=kwargs["tavaghofs"] 
            for tavaghof_ in tavaghofs:
                tavaghof=Tavaghof()
                tavaghof.cause=tavaghof_['cause']
                tavaghof.duration=tavaghof_['duration']
                tavaghof.description=tavaghof_['description']
                tavaghof.vehicle_hour=tavaghof_['vehicle_hour']
                tavaghof.work_shift=work_shift
                tavaghof.save()
 
                
        if 'products' in kwargs and result==SUCCEED:
            products=kwargs["products"] 
            for product_ in products:
                product=Product()
                product.name=product_['name']
                product.quantity=product_['quantity']
                product.description=product_['description']
                product.unit_price=product_['unit_price']
                product.service_man=product_['service_man']
                product.anbar=product_['anbar']
                product.work_shift=work_shift
                product.save()
 
                

        return result,message,work_shift

    
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
        if "owner_id" in kwargs:
            owner_id=kwargs["owner_id"]
            objects=objects.filter(owner_id=owner_id)  
        return objects.all()
        
    def vehicle(self,*args, **kwargs):
        if "vehicle_id" in kwargs and kwargs["vehicle_id"] is not None:
            return self.objects.filter(pk=kwargs['vehicle_id']).first()  
        if "vehicle_code" in kwargs and kwargs["vehicle_code"] is not None:
            return self.objects.filter(vehicle_code=kwargs['vehicle_code']).first()  
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
        if 'brand_name' in kwargs:
            vehicle.brand_name=kwargs["brand_name"]
        if 'model_name' in kwargs:
            vehicle.model_name=kwargs["model_name"]
        if 'vehicle_type' in kwargs:
            vehicle.vehicle_type=kwargs["vehicle_type"]
        if 'vehicle_color' in kwargs:
            vehicle.vehicle_color=kwargs["vehicle_color"]
        if 'vehicle_code' in kwargs:
            vehicle.vehicle_code=kwargs["vehicle_code"]
        if 'plaque' in kwargs:
            vehicle.plaque=kwargs["plaque"]
        if 'year' in kwargs:
            vehicle.year=kwargs["year"]
        if 'kilometer' in kwargs:
            vehicle.kilometer=kwargs["kilometer"]
        if 'driver_id' in kwargs:
            driver_id=kwargs["driver_id"]
            if driver_id is not None and driver_id>0:
                driver=DriverRepo(request=self.request).driver(driver_id=driver_id)
                if driver is not None:
                    vehicle.driver=driver.person_account.person.full_name
          
        if 'price' in kwargs:
            vehicle.price=kwargs["price"]
        
        (result,message,vehicle)=vehicle.save()
        return result,message,vehicle


class DriverRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Driver.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=Driver.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "owner_id" in kwargs:
            owner_id=kwargs["owner_id"]
            objects=objects.filter(owner_id=owner_id)  
        return objects.all()
        
    def driver(self,*args, **kwargs):
        if "driver_id" in kwargs and kwargs["driver_id"] is not None:
            return self.objects.filter(pk=kwargs['driver_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_driver(self,*args,**kwargs):
        result,message,driver=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_driver"):
            message="دسترسی غیر مجاز"
            return result,message,driver

        driver=Driver()
        if 'title' in kwargs:
            driver.title=kwargs["title"]
            if len(Driver.objects.filter(title=driver.title))>0:
                message='نام تکراری برای وسیله نقلیه جدید'
                return FAILED,message,None
        if 'owner_id' in kwargs:
            driver.owner_id=kwargs["owner_id"]
        if 'brand_name' in kwargs:
            driver.brand_name=kwargs["brand_name"]
        if 'model_name' in kwargs:
            driver.model_name=kwargs["model_name"]
        if 'driver_type' in kwargs:
            driver.driver_type=kwargs["driver_type"]
        if 'driver_color' in kwargs:
            driver.driver_color=kwargs["driver_color"]
        if 'driver_code' in kwargs:
            driver.driver_code=kwargs["driver_code"]
        if 'plaque' in kwargs:
            driver.plaque=kwargs["plaque"]
        if 'year' in kwargs:
            driver.year=kwargs["year"]
        if 'kilometer' in kwargs:
            driver.kilometer=kwargs["kilometer"]
        if 'driver_id' in kwargs:
            if kwargs['driver_id']>0:
                driver.driver_id=kwargs["driver_id"]
          
        (result,message,driver)=driver.save()
        return result,message,driver


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
            
        if 'driver_id' in kwargs:
            maintenance.driver_id=kwargs["driver_id"]

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

  
class VehicleEventRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=VehicleEvent.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=VehicleEvent.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(person_account__person__full_name__contains=search_for)    )
        if "vehicle_id" in kwargs:
            vehicle_id=kwargs["vehicle_id"]
            objects=objects.filter(vehicle_id=vehicle_id)  
        return objects.all()
        
    def vehicle_event(self,*args, **kwargs):
        if "vehicle_event_id" in kwargs and kwargs["vehicle_event_id"] is not None:
            return self.objects.filter(pk=kwargs['vehicle_event_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_vehicle_event(self,*args,**kwargs):
        result,message,vehicle_event=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_vehicle_event"):
            message="دسترسی غیر مجاز"
            return result,message,vehicle_event
        if len(VehicleEvent.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='قبلا برای این شخص سرویس کار ایجاد شده است.'
            return FAILED,message,None
        vehicle_event=VehicleEvent() 
        if 'person_account_id' in kwargs:
            vehicle_event.person_account_id=kwargs["person_account_id"]
          
        (result,message,vehicle_event)=vehicle_event.save()
        return result,message,vehicle_event


class TavaghofRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Tavaghof.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=Tavaghof.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(person_account__person__full_name__contains=search_for)    )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "vehicle_id" in kwargs:
                    vehicle_id=kwargs["vehicle_id"]
                    objects=objects.filter(vehicle_id=vehicle_id) 
        return objects.all()
        
    def tavaghof(self,*args, **kwargs):
        if "tavaghof_id" in kwargs and kwargs["tavaghof_id"] is not None:
            return self.objects.filter(pk=kwargs['tavaghof_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_tavaghof(self,*args,**kwargs):
        result,message,tavaghof=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_tavaghof"):
            message="دسترسی غیر مجاز"
            return result,message,tavaghof
        if len(Tavaghof.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='قبلا برای این شخص سرویس کار ایجاد شده است.'
            return FAILED,message,None
        tavaghof=Tavaghof() 
        if 'person_account_id' in kwargs:
            tavaghof.person_account_id=kwargs["person_account_id"]
          
        (result,message,tavaghof)=tavaghof.save()
        return result,message,tavaghof



 
class ServiceRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Service.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=Service.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(person_account__person__full_name__contains=search_for)    )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "vehicle_id" in kwargs:
                    vehicle_id=kwargs["vehicle_id"]
                    objects=objects.filter(vehicle_id=vehicle_id) 
        return objects.all()
        
    def service(self,*args, **kwargs):
        if "service_id" in kwargs and kwargs["service_id"] is not None:
            return self.objects.filter(pk=kwargs['service_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_service(self,*args,**kwargs):
        result,message,service=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_service"):
            message="دسترسی غیر مجاز"
            return result,message,service
        if len(Service.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='قبلا برای این شخص سرویس کار ایجاد شده است.'
            return FAILED,message,None
        service=Service() 
        if 'person_account_id' in kwargs:
            service.person_account_id=kwargs["person_account_id"]
          
        (result,message,service)=service.save()
        return result,message,service
 
class AnbarProductRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=AnbarProduct.objects.filter(id=0)
        profile=PersonRepo(request=request).me
        if profile is not None:
            if request.user.has_perm(APP_NAME+".view_vehicle"):
                self.objects=AnbarProduct.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(person_account__person__full_name__contains=search_for)    )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
         

        if "vehicle_code" in kwargs and kwargs['vehicle_code']:
            objects=objects.filter(vehicle__vehicle_code=kwargs["vehicle_code"])  
        if "driver_id" in kwargs and kwargs["driver_id"]:
            objects=objects.filter(driver_id=kwargs["driver_id"]) 
        return objects.all()
        
    def anbar_product(self,*args, **kwargs):
        if "anbar_product_id" in kwargs and kwargs["anbar_product_id"] is not None:
            return self.objects.filter(pk=kwargs['anbar_product_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_anbar_product(self,*args,**kwargs):
        result,message,anbar_product=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_anbar_product"):
            message="دسترسی غیر مجاز"
            return result,message,anbar_product
        if len(AnbarProduct.objects.filter(person_account_id=kwargs["person_account_id"]))>0:
            message='قبلا برای این شخص سرویس کار ایجاد شده است.'
            return FAILED,message,None
        anbar_product=AnbarProduct() 
        if 'person_account_id' in kwargs:
            anbar_product.person_account_id=kwargs["person_account_id"]
        
        (result,message,anbar_product)=anbar_product.save()
        return result,message,anbar_product
  