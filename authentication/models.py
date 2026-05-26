from django.db import models
from django.utils.translation import gettext as _
from .enums import *
from django.conf import settings
from utility.models import LinkHelper
from phoenix.settings import MEDIA_URL,STATIC_URL,SITE_URL
from .apps import APP_NAME
from utility.models import ImageHelper
from utility.constants import FAILED,SUCCEED
IMAGE_FOLDER=APP_NAME+"/images/"
from django.shortcuts import reverse
from utility.enums import *
 

class Person(models.Model,ImageHelper,LinkHelper):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,null=True,blank=True)
    prefix=models.CharField(_("پیشوند"),default=PersonPrefixEnum.MR,choices=PersonPrefixEnum.choices, max_length=50)
    title=models.CharField(_("عنوان"),null=True,blank=True, max_length=50)
    first_name=models.CharField(_("نام"),null=True,blank=True, max_length=50)
    last_name=models.CharField(_("نام خانوادگی"),null=True,blank=True, max_length=50)
    email=models.CharField(_("email"),null=True,blank=True, max_length=50)
    bio=models.CharField(_("بیو"),null=True,blank=True, max_length=50)
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=200)
    full_name=models.CharField(_("full_name"),null=True,blank=True, max_length=150)
    image_origin=models.ImageField(_("تصویر"),null=True,blank=True, upload_to=IMAGE_FOLDER+"person/", height_field=None, width_field=None, max_length=None)
    gender=models.CharField(_("جنسیت"),choices=GenderEnum.choices,default=GenderEnum.MALE, max_length=50)
    type=models.CharField(_("ماهیت"),choices=PersonTypeEnum.choices,default=PersonTypeEnum.FREE, max_length=50)
    type2=models.CharField(_("نوع"),choices=PersonType2Enum.choices,default=PersonType2Enum.HAGHIGHI, max_length=50)
    economic_no=models.CharField(_("شماره اقتصادی"),null=True,blank=True, max_length=20)
    melli_code=models.CharField(_("کد ملی"),null=True,blank=True, max_length=12)
    tel=models.CharField(_("تلفن"),null=True,blank=True, max_length=50)
    mobile=models.CharField(_("موبایل"),null=True,blank=True, max_length=50)
    postal_code=models.CharField(_("کد پستی"),null=True,blank=True, max_length=20)
    birth_date=models.CharField(_("تاریخ تولد"),null=True,blank=True, max_length=20)
    birth_location=models.CharField(_("محل تولد"),null=True,blank=True, max_length=20)
    father_name=models.CharField(_("نام پدر"),null=True,blank=True, max_length=20)
 
    
    class_name='person'
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
    def get_accounting_absolute_url(self):
        from django.shortcuts import reverse
        return reverse('accounting:person',kwargs={'pk':self.pk})
   
    @property
    def full_name_(self):
        full_name=""
        if self.prefix:
            full_name=self.prefix+" "
             
        if self.title:
            full_name+=self.title +" "
           
        if self.first_name:
            full_name+=self.first_name +" "

             
            
           
        if self.last_name:
            full_name+=self.last_name +" "
            

            
             

        return full_name.replace('  ',' ')



    def __str__(self):
        return self.full_name

    def username(self):
        if self.user is not None:
            return self.user.username

   
    def user_id(self):
        if self.user is not None:
            return self.user.id

   

    def save(self,*args, **kwargs):
        result,message,person=FAILED,"",None
        # others=Person.objects.exclude(pk=self.pk)
        # if others.filter(code=self.code).first() is not None:
        #     message="کد تکراری می باشد."
        #     return result,message,person
        # self.
        # 
         
        self.full_name=self.full_name_
        persons=Person.objects.filter(full_name=self.full_name)
        if self.id is None:
            if len(persons)>0:
                message='نام تکراری برای شخص'
                return FAILED,message,None
        if len(persons.exclude(pk=self.pk))>0:
                message='نام تکراری برای شخص'
                return FAILED,message,None
        super(Person,self).save()
        result=SUCCEED
        message=" با موفقیت اضافه گردید."
        person=self
        return result,message,person 

    def image(self):
        if self.image_origin is None or str(self.image_origin)=='':
            return f'{STATIC_URL}{APP_NAME}/img/person.png'
        
        return f'{MEDIA_URL}{self.image_origin}'
    def get_change_password_url(self):
        return reverse(APP_NAME+":change_user_password",kwargs={'pk':self.pk})
Profile=Person




class MyLink(models.Model,LinkHelper):
    person=models.ForeignKey("person", verbose_name=_("person"), on_delete=models.CASCADE)
    title = models.CharField(_("url"), max_length=2000)
    url = models.CharField(_("url"), max_length=2000)
    priority = models.IntegerField(_("priority"), default=100)
    
    class_name='mylink'
    app_name=APP_NAME
    
    class Meta:
        verbose_name = _("MyLink")
        verbose_name_plural = _("MyLinks")

    def __str__(self):
        return f"{self.person} : {self.title}"
 

class ClipBoardItem(models.Model):
    name=models.CharField(_("name"), max_length=100)
    text=models.CharField(_("text"), max_length=100)
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("ClipBoardItem")
        verbose_name_plural = _("ClipBoardItems")

    def __str__(self):
 
        return f'{self.person}  :  {self.name} :  {self.text}'
