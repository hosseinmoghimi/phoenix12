from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY,MEDIA_URL
from utility.models import LinkHelper,ImageHelper
from .apps import APP_NAME
IMAGE_FOLDER=APP_NAME+"/images/"

class Blog(Page):
    for_home=models.BooleanField(_("for home"), default=False)
    start_date=models.DateTimeField(_("start_date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("end_date"),null=True,blank=True, auto_now=False, auto_now_add=False)


    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
 
 

    def save(self):
         if self.class_name is None or self.class_name=='':
             self.class_name='blog'
         if self.app_name is None or self.app_name=='':
             self.app_name=APP_NAME

         (result,message,blog)=FAILED,'',self
         super(Blog,self).save()
         result=SUCCEED
         message='بلاگ با موفقیت ذخیره شد.'
         return  (result,message,blog)
 
class HomeSlider(models.Model,ImageHelper,LinkHelper):
    image_origin = models.ImageField(_("تصویر اسلایدر  1333*2000 "), upload_to=IMAGE_FOLDER +
                                     'Banner/', height_field=None, width_field=None, max_length=None)
    title = models.CharField(_("عنوان"), null=True, blank=True, max_length=500)
    body = models.TextField(_("بدنه"), null=True, blank=True, max_length=2000)
    text_color = models.CharField(_("رنگ متن"), default="#fff", max_length=20)

    priority = models.IntegerField(_("ترتیب"), default=100)
    archive = models.BooleanField(_("بایگانی شود؟"), default=False)
    tag_number = models.IntegerField(_("عدد برچسب"), default=100)
    tag_text = models.CharField(
        _("متن برچسب"), max_length=100, blank=True, null=True)
    app_name=APP_NAME
    class_name="homeslider"
    class Meta:
        verbose_name = _("HomeSlider")
        verbose_name_plural = _("HomeSliders")
 
    def __str__(self):
        return str(self.priority)
 