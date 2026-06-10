from django.db import models
from utility.models import LinkHelper,DateTimeHelper,DateHelper
from accounting.models import UnitNameEnum,CorePage,FAILED,SUCCEED
from phoenix.settings import MEDIA_URL
from .apps import APP_NAME
from accounting.models import Asset, FinancialEvent
from utility.currency import to_price
from phoenix.server_settings import CURRENCY
from utility.calendar import PERSIAN_MONTH_NAMES, PersianCalendar, to_persian_datetime_tag
from phoenix.settings import STATIC_URL
from django.db import models
from core.models import  Page,ColorEnum,Event
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME 
from .enums import * 
from accounting.models import Invoice,InvoiceLine

  
class ServiceMan(models.Model,LinkHelper):
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person_account"), on_delete=models.CASCADE)
    class_name='serviceman'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("ServiceMan")
        verbose_name_plural = _("ServiceMans")
    @property
    def title(self):
        return self.person_account.person.full_name
    def __str__(self):
        return str(self.title)
    def save(self,*args, **kwargs):
        result,message,service_man=FAILED,'',None
        if self.title is None or self.title=="":
            self.title=self.account.title
        super(ServiceMan,self).save(*args, **kwargs)
        message='سرویس کار با موفقیت اضافه شد.'
        return SUCCEED,message,self


class Maintenance(Event):
    kilometer=models.IntegerField(_("کیلومتر"),default=0)
    service_man=models.ForeignKey("serviceman", verbose_name=_("service man"), on_delete=models.PROTECT)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.PROTECT)
    maintenance_type=models.CharField(_("سرویس"),choices=MaintenanceTypesEnum.choices, max_length=100)
    
    invoices=models.ManyToManyField("accounting.invoice",blank=True, verbose_name=_("invoice"))
    
    class_name='maintenance'
    app_name=APP_NAME


    @property
    def sum(self):
        sum=0
        for invoice in self.invoices.all():
            if invoice.valid:
                sum+=invoice.amount
        return sum
    def save(self, *args, **kwargs):
        
        from django.utils import timezone
        now =timezone.now()
        if self.event_datetime is None:
            self.event_datetime=now
        if self.start_datetime is None:
            self.start_datetime=now
        if self.end_datetime is None:
            self.end_datetime=now

        if self.app_name is None or self.app_name=="":
            self.app_name = APP_NAME
        if self.class_name is None or self.class_name=="":
            self.class_name = "maintenance"
        return super(Maintenance, self).save(*args, **kwargs)
    class Meta:
        verbose_name = _("Maintenance")
        verbose_name_plural = _("Maintenances")
 
    def all_invocie_lines(self):
        invoice_ids=[]
        for invoice in self.invoices.all():
            invoice_ids.append(invoice.id)
        return InvoiceLine.objects.filter(invoice_id__in=invoice_ids).order_by('invoice_id')


class MaintenanceInvoice(Invoice):
    kilometer=models.IntegerField(_("کیلومتر"),default=0)
    service_man=models.ForeignKey("serviceman", verbose_name=_("service man"), on_delete=models.PROTECT)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.PROTECT)
    maintenance_type=models.CharField(_("سرویس"),choices=MaintenanceTypesEnum.choices, max_length=100)
    class Meta:
        verbose_name = _("MaintenanceInvoice")
        verbose_name_plural = _("MaintenanceInvoices")
    def save(self,*args, **kwargs):
        result,message,self=FAILED,'',self
        if self.title is None or self.title=="":
            self.title=self.maintenance_type
        if self.class_name is None or self.class_name=="":
            self.class_name='maintenanceinvoice'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        result,message,inv=super(MaintenanceInvoice,self).save(*args, **kwargs)
        result=SUCCEED
        message='با موفقیت اضافه شد.'    
        return (result,message,self)
    
    def __str__(self):
        return f'{self.service_man} {self.maintenance_type} {self.vehicle}'
 
  
class Vehicle(Asset):
    vehicle_type=models.CharField(_("نوع وسیله "),choices=VehicleTypeEnum.choices,default=VehicleTypeEnum.SEDAN, max_length=50)
    brand_name=models.CharField(_("برند"),choices=VehicleBrandEnum.choices,default=VehicleBrandEnum.IRAN_KHODRO, max_length=50)
    model_name=models.CharField(_("مدل"),null=True,blank=True, max_length=50)
    plaque=models.CharField(_("پلاک"),null=True,blank=True, max_length=50)
    driver=models.CharField(_("راننده"), max_length=50,null=True,blank=True)
    year=models.CharField(_("سال"), max_length=50,null=True,blank=True)
    vehicle_color=models.CharField(_("رنگ"),choices=VehicleColorEnum.choices,default=VehicleColorEnum.SEFID, max_length=50)
    kilometer=models.IntegerField(_("کیلومتر"),default=0)
 
    def save(self,*args, **kwargs): 
        (result,message,vehicle)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="vehicle"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Vehicle,self).save()   
        result=SUCCEED
        message="وسیله نقلیه با موفقیت اضافه شد."
        return (result,message,vehicle)
    
    class Meta:
        verbose_name = _("Vehicle")
        verbose_name_plural = _("Vehicles")

    def get_trips_url(self):
        return reverse(APP_NAME+":trips",kwargs={'category_id':0,'driver_id':0,'passenger_id':0,'vehicle_id':self.pk,'trip_path_id':0})
      

    def thumbnail(self):
        if self.thumbnail_origin is not None:
            return MEDIA_URL+str(self.thumbnail_origin)
        pic='trailer.jpg'
        if self.vehicle_type==VehicleTypeEnum.TRAILER:
            pic='trailer.jpg'
        if self.vehicle_type==VehicleTypeEnum.TRUCK:
            pic='truck.jpg'
        if self.vehicle_type==VehicleTypeEnum.TAXI:
            pic='taxi.jpg'
        if self.vehicle_type==VehicleTypeEnum.LOADER:
            pic='loader.jpg'
        if self.vehicle_type==VehicleTypeEnum.SEDAN:
            pic='sedan.jpg'
        if self.vehicle_type==VehicleTypeEnum.BUS:
            pic='bus.jpg'
        if self.vehicle_type==VehicleTypeEnum.GRADER:
            pic='grader.jpg'
        return f'{STATIC_URL}{APP_NAME}/images/thumbnail/{pic}/' 


 