from django.db import models
from django.utils.translation import gettext as _
from phoenix.settings import ADMIN_URL,STATIC_URL,MEDIA_URL
from django.shortcuts import reverse 
from .calendar import PersianCalendar
from .apps import APP_NAME
IMAGE_FOLDER = APP_NAME+"/images/"


class DateHelper():
    def persian_start_date(self):
        return PersianCalendar().from_gregorian(self.start_date)
    def persian_end_date(self):
        return PersianCalendar().from_gregorian(self.end_date)
    def persian_date(self):
        return PersianCalendar().from_gregorian(self.date)
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    def persian_date_created(self):
        return PersianCalendar().from_gregorian(self.date_created)
    def persian_date_modified(self):
        return PersianCalendar().from_gregorian(self.date_modified)
    def persian_expiration_date(self):
        return PersianCalendar().from_gregorian(self.expiration_date)
    def persian_production_date(self):
        return PersianCalendar().from_gregorian(self.production_date)
 

class DateTimeHelper(DateHelper):
    def persian_enter_datetime(self):
        return PersianCalendar().from_gregorian(self.enter_datetime)
    def persian_date_time(self):
        return PersianCalendar().from_gregorian(self.date_time)
    def persian_exit_datetime(self):
        return PersianCalendar().from_gregorian(self.exit_datetime)
    def persian_start_datetime(self):
        return PersianCalendar().from_gregorian(self.start_datetime)
    def persian_end_datetime(self):
        return PersianCalendar().from_gregorian(self.end_datetime)
    def persian_datetime(self):
        return PersianCalendar().from_gregorian(self.datetime)
    def persian_transaction_datetime(self):
        return PersianCalendar().from_gregorian(self.transaction_datetime)
    def persian_print_datetime(self):
        return PersianCalendar().from_gregorian(self.print_datetime)
    def persian_datetime_added(self):
        return PersianCalendar().from_gregorian(self.datetime_added) 
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added) 
    def persian_document_datetime(self):
        return PersianCalendar().from_gregorian(self.document_datetime)
    def persian_event_datetime(self):
        return PersianCalendar().from_gregorian(self.event_datetime)

    def persian_event_datetime(self):
        return PersianCalendar().from_gregorian(self.event_datetime)

    def persian_start_datetime(self):
        return PersianCalendar().from_gregorian(self.start_datetime)
    
    def persian_date_updated(self):
        return PersianCalendar().from_gregorian(self.date_updated)

    def persian_end_datetime(self):
        return PersianCalendar().from_gregorian(self.end_datetime)

    def start_datetime2(self):
        return self.start_datetime.strftime("%Y-%m-%d %H:%M")

    def end_datetime2(self):
        return self.end_datetime.strftime("%Y-%m-%d %H:%M")


class ImageHelper:
    @property
    def image(self):
        image=""
        try:
            sss=self.image_origin
        except:
            return self.thumbnail

        if self.image_origin is None or str(self.image_origin)=="":
            try:
                image= f"{STATIC_URL}{self.app_name}/img/pages/image/{self.class_name}.png/"
            except:
                pass
        else:
            image= f"{MEDIA_URL}{self.image_origin}"

        return image
    @property
    def thumbnail(self):
         
        thumbnail=""
        if self.thumbnail_origin is None or str(self.thumbnail_origin)=="":
            try:
                thumbnail= f"{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png/"
            except:
                pass
        else:
            thumbnail= f"{MEDIA_URL}{self.thumbnail_origin}"

        return thumbnail
    

    @property
    def logo(self):
        logo=""
        if self.logo_origin is None or str(self.logo_origin)=="":
            try:
                logo= f"{STATIC_URL}{self.app_name}/img/pages/logo/{self.class_name}.png/"
            except:
                pass
        else:
            logo= f"{MEDIA_URL}{self.logo_origin}"

        return logo
    

    @property
    def header(self):
        header=""
        if self.header_origin is None or str(self.header_origin)=="":
            try:
                header= f"{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png/"
            except:
                pass
        else:
            header= f"{MEDIA_URL}{self.header_origin}"

        return header


class LinkHelper():
    def get_edit_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/"
    def get_absolute_url(self):
        return reverse(f"{self.app_name}:{self.class_name}",kwargs={'pk':self.pk})
    def get_delete_url(self):
        return f"{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/delete/"
        
    def get_edit_url_admin(self):
        return f'{ADMIN_URL}{self.app_name}/{self.class_name}/{self.pk}/change/'


    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="ویرایش" href="{self.get_edit_url()}"><i class="fa fa-edit text-warning"></i></a>
        """
    def get_delete_btn(self):
        return f"""
          <a target="_blank" title="حذف" href="{self.get_delete_url()}"><i class="fa fa-trash text-danger"></i></a>
        """


class Picture(models.Model, LinkHelper):
    app_name = models.CharField(_("app_name"), max_length=50)
    name = models.CharField(_("name"), max_length=50)
    image_origin = models.ImageField(_("image"), upload_to=IMAGE_FOLDER+"pictures/",
                                     null=True, blank=True, height_field=None, width_field=None, max_length=None)
    class_name = "picture"

    @property
    def image(self):
        if self.image_origin and self.image_origin is not None:
            return f'{MEDIA_URL}{str(self.image_origin)}'
        if self.image_origin =="":
            return f'{STATIC_URL}logo.png'
        if self.image_origin is None:
            return f'{STATIC_URL}logo.png'
        return None

    class Meta:
        verbose_name = _("Picture")
        verbose_name_plural = _("Pictures")

    def __str__(self):
        return self.app_name+" : "+self.name

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/picture/{self.pk}/change/"
 

class Parameter(models.Model):
    app_name = models.CharField(_("app_name"), max_length=50)
    name = models.CharField(_("نام پارامتر (تغییر ندهید)"), max_length=50)
    origin_value = models.CharField(
        _("مقدار پارامتر"), null=True, blank=True, max_length=50000)
    class_name = "parameter"

    @property
    def value(self):
        if self.origin_value is None:
            return ''
        return self.origin_value
    
    
    @property
    def int_value(self):
        if self.origin_value is None:
            return 0
        return int(self.origin_value)


    @property
    def boolean_value(self):
        if self.origin_value is None:
            return False
        if self.origin_value == 'True':
            return True
        if self.origin_value == '1':
            return True
        if self.origin_value == 'true':
            return True
        if self.origin_value == 'بله':
            return True
        if self.origin_value == 'درست':
            return True
        if self.origin_value == 'آری':
            return True
        return False

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")

    def __str__(self):
        return self.app_name+":"+self.name

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/change/"

    def get_delete_url(self):
        return f"{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/delete/"

    def get_edit_btn(self):
        return f"""
            <a title="ویرایش" target="_blank" href="{self.get_edit_url()}">
                <i class="fa fa-edit text-info mx-2"></i>
            </a>
        """
 

class State(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    priority=models.IntegerField(_("priority"),default=1000)

    app_name=APP_NAME
    class_name="state"

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")

    def __str__(self):
        return self.name 
    
    
class City(models.Model,LinkHelper):
    state=models.ForeignKey("state", verbose_name=_("state"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=50)
    priority=models.IntegerField(_("priority"),default=1000)

    app_name=APP_NAME
    class_name="city"

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Citys")

    def __str__(self):
        return self.name 
    
    
class Region(models.Model,LinkHelper):
    city=models.ForeignKey("city", verbose_name=_("city"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=50)
    priority=models.IntegerField(_("priority"),default=1000)
    app_name=APP_NAME
    class_name="region"
    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return self.name 
