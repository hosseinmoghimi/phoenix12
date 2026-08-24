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
    work_shift=models.ForeignKey("workshift", verbose_name=_("workshift"), on_delete=models.PROTECT)
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
        return f'{self.pk} - {self.work_shift} / {self.filter_action} {self.count} {self.filter_type} '
 
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

    @property
    def vehicle(self):
        return self.oiling_maintenance.vehicle


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
    vehicle_event_type=models.CharField(_("vehicle_event_type"), max_length=50)
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

    start_kilometer=models.IntegerField(_("کیلومتر شروع"),null=True,blank=True)
    end_kilometer=models.IntegerField(_("کیلومتر پایان"),null=True,blank=True)

    load=models.CharField(_("load"),null=True,blank=True, max_length=50)
    count=models.IntegerField(_("count"),default=0)


    class Meta:
        verbose_name = _("Karkerd")
        verbose_name_plural = _("Karkerds")
 
    def save(self,*args, **kwargs): 
        self.vehicle_event_type="کارکرد"
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
        self.vehicle_event_type="توقف"
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
    location=models.ForeignKey("attachments.location", verbose_name=_("location"),null=True,blank=True, on_delete=models.SET_NULL)
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


class WorkShift(models.Model,LinkHelper): 
    class_name="workshift"
    app_name=APP_NAME
     
    vehicle=models.ForeignKey("vehicle", verbose_name=_("vehicle"), on_delete=models.PROTECT)
    driver=models.ForeignKey("driver", verbose_name=_("driver"), on_delete=models.PROTECT)
    shift_date=models.DateField(_("shift_date"), auto_now=False, auto_now_add=False)
    shift=models.CharField(_("shift"), max_length=50)
    start_hour=models.IntegerField(_("start_hour"), default=0)
    end_hour=models.IntegerField(_("end_hour"), default=0)


    
    vehicle_start_hour=models.FloatField(_("vehicle_start_hour"), default=0)
    vehicle_end_hour=models.FloatField(_("vehicle_end_hour"), default=0)

    
    location=models.CharField(_("location"), max_length=50)
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)



    oil_type=models.CharField(_("oil_type"), max_length=50)
    oil_liter=models.IntegerField(_("oil_liter"), default=0)
    gasoil_liter=models.IntegerField(_("gasoil_liter"), default=0)
    vehicle_hour=models.IntegerField(_("vehicle_hour"), default=0)
    
    oil_service=models.CharField(_("oil_service"), max_length=50)

    tavaghof_cause=models.CharField(_("tavaghof_cause"),null=True,blank=True, max_length=50)
    tavaghof_duration=models.IntegerField(_("tavaghof_duration"), default=0)
    tavaghof_description=models.CharField(_("tavaghof_description"),null=True,blank=True, max_length=500)

  
    kharabi_duration=models.IntegerField(_("kharabi_duration"), default=0)
    kharabi_description=models.CharField(_("kharabi_description"),null=True,blank=True, max_length=500)
 
    class Meta:
        verbose_name = _("WorkShift")
        verbose_name_plural = _("WorkShifts")

    def __str__(self):
        return f'{self.vehicle.vehicle_code}  {self.vehicle}  {PersianCalendar().from_gregorian(self.shift_date)} {self.shift}'
    @property
    def title(self):
        return self.__str__()
    def save(self,*args, **kwargs): 
        
        (result,message,workshift)=FAILED,'',self
         
        super(WorkShift,self).save()   
        result=SUCCEED
        message="شیفت کاری دستگاه با موفقیت ذخیره شد."
        return (result,message,workshift)


class OilService(models.Model,LinkHelper):
    class_name="oilservice"
    app_name=APP_NAME
    work_shift=models.ForeignKey("workshift", verbose_name=_("workshift"), on_delete=models.PROTECT)
    oil_type=models.CharField(_("oil_type"), max_length=50)
    oil_action=models.CharField(_("oil_action"),max_length=50)
    oil_liter=models.FloatField(_("oil_liter"),default=1)
    vehicle_hour=models.FloatField(_("vehicle_hour"),default=0)

    class Meta:
        verbose_name = _("OilService")
        verbose_name_plural = _("OilServices")
 
    def __str__(self):
        return f'{self.work_shift} / {self.oil_type} {self.oil_action} {self.oil_liter} '
 
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

    @property
    def vehicle(self):
        return self.work_shift.vehicle


class FilterService(models.Model,LinkHelper):
    class_name='filterservice'
    app_name=APP_NAME
    work_shift=models.ForeignKey("workshift", verbose_name=_("workshift"), on_delete=models.PROTECT)
    filter_type=models.CharField(_("filter type"),choices=FilterTypeEnum.choices, max_length=50)
    filter_action=models.CharField(_("filter action"), choices=FilterActionEnum.choices,max_length=50)
    count=models.IntegerField(_("count"),default=1)
    cost=models.IntegerField(_("cost"),default=0)
    
    description=models.CharField(_("description"),null=True,blank=True, max_length=500)


    class Meta:
        verbose_name = _("FilterService")
        verbose_name_plural = _("FilterServices")

    def __str__(self):
        return f'{self.work_shift} / {self.filter_action} {self.count} {self.filter_type} '
 
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

    @property
    def vehicle(self):
        return self.work_shift.vehicle


class Tavaghof(models.Model,LinkHelper):
    class_name="tavaghof"
    app_name=APP_NAME
    work_shift=models.ForeignKey("workshift", verbose_name=_("workshift"), on_delete=models.PROTECT)
    cause=models.CharField(_("cause"), max_length=50)
    duration=models.FloatField(_("duration"),default=1)
    descriptin=models.CharField(_("descriptin"),max_length=50)
    vehicle_hour=models.FloatField(_("vehicle_hour"),default=0)


    class Meta:
        verbose_name = _("Tavaghof")
        verbose_name_plural = _("Tavaghofs")

    def __str__(self):
        return self.name


class Product(models.Model,LinkHelper):
    class_name="product"
    app_name=APP_NAME
    work_shift=models.ForeignKey("workshift", verbose_name=_("workshift"), on_delete=models.PROTECT)
    product=models.CharField(_("product"), max_length=50)
    quantity=models.IntegerField(_("quantity"),default=1)
    unit_price=models.IntegerField(_("unit_price"),default=0)
    anbar=models.CharField(_("anbar"),max_length=50)
    service_man=models.CharField(_("service_man"),max_length=50)
    description=models.CharField(_("description"),max_length=50)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name
 