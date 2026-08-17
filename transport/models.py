from tinymce.models import HTMLField
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


class Driver(models.Model,LinkHelper):
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person_account"), on_delete=models.CASCADE)
    class_name='driver'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Driver")
        verbose_name_plural = _("Drivers")
    @property
    def title(self):
        return self.person_account.person.full_name
    def __str__(self):
        return str(self.title)
    def save(self,*args, **kwargs):
        result,message,driver=FAILED,'',None
        if self.title is None or self.title=="":
            self.title=self.account.title
        super(Driver,self).save(*args, **kwargs)
        message='سرویس کار با موفقیت اضافه شد.'
        return SUCCEED,message,self


class Maintenance(Event):
    maintenance_type=models.CharField(_("سرویس"),choices=MaintenanceTypesEnum.choices, max_length=100)
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.PROTECT)
    service_man=models.ForeignKey("serviceman", verbose_name=_("service man"), on_delete=models.PROTECT)
    driver=models.ForeignKey("driver", verbose_name=_("driver"),blank=True,null=True, on_delete=models.PROTECT)
    hour=models.IntegerField(_("hour"),default=0)
    kilometer=models.IntegerField(_("کیلومتر"),default=0)
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


class OilingMaintenance(Maintenance):
    oil_type=models.CharField(_("oil type"),choices=OilTypeEnum.choices, max_length=50)
    oil_liter=models.FloatField(_("oil liter")) 
    fuel_liter=models.FloatField(_("fuel liter")) 
    replace_oil=models.BooleanField(_("replace oil"))
    over_load_oil=models.BooleanField(_("over load oil"))


    class_name='oilingmaintenance'
    app_name=APP_NAME
    class Meta:
        verbose_name = _("OilingMaintenance")
        verbose_name_plural = _("OilingMaintenances")
 
    def save(self, *args, **kwargs):
        
        if self.app_name is None or self.app_name=="":
            self.app_name = APP_NAME
        if self.class_name is None or self.class_name=="":
            self.class_name = "oilingmaintenance"
        return super(OilingMaintenance, self).save(*args, **kwargs)


class OilingMaintenanceDetail(models.Model,LinkHelper):
    oiling_maintenance=models.ForeignKey("oilingmaintenance", verbose_name=_("oiling_maintenance"), on_delete=models.CASCADE)
    filter_type=models.CharField(_("filter type"),choices=FilterTypeEnum.choices, max_length=50)
    filter_action=models.CharField(_("filter action"), choices=FilterActionEnum.choices,max_length=50)
    count=models.IntegerField(_("count"),default=1)
    cost=models.IntegerField(_("cost"),default=0)
    
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)

    class_name='oilingmaintenancedetail'
    app_name=APP_NAME
    class Meta:
        verbose_name = _("OilingMaintenanceDetail")
        verbose_name_plural = _("OilingMaintenanceDetails")

    def __str__(self):
        return f'{self.pk} - {self.oiling_maintenance} / {self.filter_action} {self.count} {self.filter_type} '
 
    def save(self,*args, **kwargs): 
         (result,message,oiling_maintenance_detail)=FAILED,'',self
         if self.class_name is None or self.class_name=="":
             self.class_name="oiling_maintenance_detail"
         if self.app_name is None or self.app_name=="":
             self.app_name=APP_NAME
         super(OilingMaintenanceDetail,self).save()   
         result=SUCCEED
         message="جزئیات روغن کاری با موفقیت اضافه شد."
         return (result,message,oiling_maintenance_detail)

    
class MaintenanceInvoice(Invoice):
    hour=models.IntegerField(_("hour"),default=0)
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
    vehicle_code=models.CharField(_("کد وسیله "), null=True,blank=True,max_length=50)
    brand_name=models.CharField(_("برند"),choices=VehicleBrandEnum.choices,default=VehicleBrandEnum.IRAN_KHODRO, max_length=50)
    model_name=models.CharField(_("مدل"),null=True,blank=True, max_length=50)
    plaque=models.CharField(_("پلاک"),null=True,blank=True, max_length=50)
    driver=models.CharField(_("راننده"), max_length=50,null=True,blank=True)
    year=models.CharField(_("سال"), max_length=50,null=True,blank=True)
    vehicle_color=models.CharField(_("رنگ"),choices=VehicleColorEnum.choices,default=VehicleColorEnum.SEFID, max_length=50)
    kilometer=models.IntegerField(_("کیلومتر"),default=0)
 
    def save(self,*args, **kwargs): 
        (result,message,vehicle)=FAILED,'',self
        if vehicle.title is None or vehicle.title=="":
                    vehicle.title=f'{vehicle.vehicle_type if vehicle.vehicle_type else ""}{  " "+vehicle.brand_name if vehicle.brand_name else "" }{ " "+vehicle.model_name if vehicle.model_name else ""}{ " - کد  "+vehicle.vehicle_code}'

        self.title=self.title.replace('  ',' ')
        if self.class_name is None or self.class_name=="":
            self.class_name="vehicle"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Vehicle,self).save()   
        result=SUCCEED
        message="وسیله نقلیه با موفقیت  ذخیره شد."
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


class VehicleEvent(Event):
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.PROTECT)
    driver=models.ForeignKey("driver", verbose_name=_("driver"),null=True,blank=True, on_delete=models.SET_NULL)
    project_name=models.CharField(_("project_name"), max_length=50,null=True,blank=True)
    area_name=models.CharField(_("area_name"), max_length=50,null=True,blank=True)
    
    # project=models.ForeignKey("projectmanager.project",related_name="ssssdsd", verbose_name=_("project"), on_delete=models.PROTECT)
    # area=models.ForeignKey("attachments.area",related_name="weewgdfg", verbose_name=_("area"),null=True,blank=True, on_delete=models.SET_NULL)
    


    class Meta:
        verbose_name = _("VehicleEvent")
        verbose_name_plural = _("VehicleEvents")
 
 
    def save(self,*args, **kwargs): 
         (result,message,vehicle_event)=FAILED,'',self
          
 
         if self.class_name is None or self.class_name=="":
             self.class_name="vehicleevent"
         if self.app_name is None or self.app_name=="":
             self.app_name=APP_NAME
         super(VehicleEvent,self).save()   
         result=SUCCEED
         message="رویداد وسیله نقلیه با موفقیت ذخیره شد."
         return (result,message,vehicle_event)


class Karkerd(VehicleEvent):
    start_hour=models.FloatField(_("ساعت شروع"))
    end_hour=models.FloatField(_("ساعت پایان"))

    start_kilometer=models.FloatField(_("کیلومتر شروع"),null=True,blank=True)
    end_kilometer=models.FloatField(_("کیلومتر پایان"),null=True,blank=True)

    load=models.CharField(_("load"),null=True,blank=True, max_length=50)
    count=models.IntegerField(_("count"),default=0)


    class Meta:
        verbose_name = _("Karkerd")
        verbose_name_plural = _("Karkerds")
 
    def save(self,*args, **kwargs): 
          (result,message,karkerd)=FAILED,'',self
           
  
          if self.class_name is None or self.class_name=="":
              self.class_name="karkerd"
          if self.app_name is None or self.app_name=="":
              self.app_name=APP_NAME
          super(Karkerd,self).save()   
          result=SUCCEED
          message="کارکرد وسیله نقلیه با موفقیت ذخیره شد."
          return (result,message,karkerd)


 
class Tavaghof(VehicleEvent):
    cause=models.CharField(_("علت"), max_length=50)
    

    class Meta:
        verbose_name = _("Tavaghof")
        verbose_name_plural = _("Tavaghofs")
 
    def save(self,*args, **kwargs): 
          (result,message,tavaghof)=FAILED,'',self
           
  
          if self.class_name is None or self.class_name=="":
              self.class_name="tavaghof"
          if self.app_name is None or self.app_name=="":
              self.app_name=APP_NAME
          super(Tavaghof,self).save()   
          result=SUCCEED
          message="توقف وسیله نقلیه با موفقیت ذخیره شد."
          return (result,message,tavaghof)


class VehicleStatus(models.Model,LinkHelper):
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.CASCADE)     
    status_datetime = models.DateTimeField(_("status_datetime"), auto_now=False, auto_now_add=False)
    locaion=models.ForeignKey("attachments.location", verbose_name=_("location"),null=True,blank=True, on_delete=models.SET_NULL)
    kilometer=models.IntegerField(_("kilometer"))
    hour=models.IntegerField(_("hour"))
    motor=models.CharField(_("motor"),null=True,blank=True, max_length=500)
    gear_box=models.CharField(_("gear_box"),null=True,blank=True, max_length=500)
    ziroband=models.CharField(_("ziroband"),null=True,blank=True, max_length=500)
    cabin=models.CharField(_("cabin"),null=True,blank=True, max_length=500)
    cooler=models.CharField(_("cooler"),null=True,blank=True, max_length=500)
    heater=models.CharField(_("heater"),null=True,blank=True, max_length=500)
    wiring=models.CharField(_("wiring"),null=True,blank=True, max_length=500)
    light=models.CharField(_("light"),null=True,blank=True, max_length=500)
    hydrolic=models.CharField(_("hydrolic"),null=True,blank=True, max_length=500)
    pakat=models.CharField(_("pakat"),null=True,blank=True, max_length=500)
    compress=models.CharField(_("compress"),null=True,blank=True, max_length=500)
    description=HTMLField(_("توضیحات کامل"),null=True,blank=True, max_length=5000)
    class_name="vehiclestatus"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("VehicleStatus")
        verbose_name_plural = _("VehicleStatuses")

    def __str__(self):
        return f'{self.vehicle} @ {PersianCalendar().from_gregorian(self.status_datetime)}'

    def persian_status_datetime(self):
        return PersianCalendar().from_gregorian(self.status_datetime)
    def short_desc(self):
        from utility.num import separate
        return f"""<span class="mr-2">کیلومتر</span><strong class="mx-2">{separate(self.kilometer)}</strong><span class="mr-2">ساعت</span><strong class="mx-1">{separate(self.hour)} </strong>"""