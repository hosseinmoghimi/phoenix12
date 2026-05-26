from django.db import models
from .apps import APP_NAME
from django.utils.translation import gettext as _
from utility.qrcode import generate_qrcode
from utility.enums import *
from .enums import *
from utility.calendar import PersianCalendar
from utility.models import LinkHelper,ImageHelper,DateTimeHelper
from tinymce.models import HTMLField
from django.shortcuts import reverse
from django.core.files.storage import FileSystemStorage
from utility.constants import FAILED,SUCCEED
from phoenix.server_settings import UPLOAD_ROOT,QRCODE_ROOT,QRCODE_URL,STATIC_URL,MEDIA_URL,ADMIN_URL,FULL_SITE_URL
IMAGE_FOLDER = "attachments/images/"
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')
 
class PagePrint(models.Model,DateTimeHelper):
    page=models.ForeignKey("core.page", verbose_name=_("page"), on_delete=models.CASCADE)
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    datetime_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    type=models.CharField(_("type"),choices=PagePrintTypeEnum.choices,default=PagePrintTypeEnum.DRAFT, max_length=50)
    printed=models.BooleanField(_("printed"), default=False)

    class Meta:
        verbose_name = _("PagePrint")
        verbose_name_plural = _("PagePrints")

    def __str__(self):
        return f"{self.person} : {self.page}"
     
    
class Comment(models.Model,DateTimeHelper,LinkHelper):
    parent=models.ForeignKey("comment",related_name='replies',null=True,blank=True, verbose_name=_("parent"), on_delete=models.CASCADE)
    page=models.ForeignKey("core.page", verbose_name=_("page"), on_delete=models.CASCADE)
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    comment=HTMLField(verbose_name="comment")
    datetime_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    class_name='comment'
    app_name=APP_NAME
    @property
    def childs(self):
        return Comment.objects.filter(parent_id=self.id)
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.person} : {self.page} : {self.comment}"
     
    @property
    def reply_to_id(self):
        if self.parent is not None:
            return self.parent.id
        return None
 

class Like(models.Model,DateTimeHelper):
    page=models.ForeignKey("core.page", verbose_name=_("page"), on_delete=models.CASCADE)
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    datetime_added=models.DateTimeField(_("datetime_added"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __str__(self):
        return f" {self.person.full_name} @ {self.page.title}"

    def my_like(self,*args, **kwargs):
        person_id=0
        if 'person_id' in kwargs:
            person_id=kwargs['person_id']
        if 'person' in kwargs:
            person=kwargs['person']
            person_id=person.id
        if 'person' in kwargs:
            person=kwargs['person']
            person_id=person.id
        if 'page' in kwargs:
            page=kwargs['page']
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
        from core.repo import PageRepo,Page
        page=Page.objects.filter(pk=page_id).first()
        my_likes=Like.objects.filter(page_id=page.id).filter(person_id=person_id)
        return len(my_likes)>0
    
    
class Icon(models.Model,LinkHelper,DateTimeHelper):
    title = models.CharField(_("title"), null=True, blank=True, max_length=300)
    icon_fa = models.CharField(
        _("icon fa"), null=True, blank=True, max_length=50)
    icon_material = models.CharField(
        _("material_icon"), null=True, blank=True, max_length=50)
    icon_svg = models.TextField(_("svg_icon"), null=True, blank=True)
    # person = models.ForeignKey("authentication.person", null=True,
                                # blank=True, verbose_name=_("person"), on_delete=models.CASCADE)
    color = models.CharField(
        _("color"), choices=ColorEnum.choices, default=ColorEnum.PRIMARY, max_length=50)
    width = models.IntegerField(_("عرض آیکون"), null=True, blank=True)
    height = models.IntegerField(_("ارتفاع آیکون"), null=True, blank=True)
    priority = models.IntegerField(_("priority"), default=1000)
    image_origin = models.ImageField(_("تصویر آیکون"), upload_to=IMAGE_FOLDER+'Icon/',
                                     height_field=None, null=True, blank=True, width_field=None, max_length=None)
    class_name='icon'
    app_name=APP_NAME
    def get_icon_tag(self, icon_style='', color=None, no_color=False):

        if color is not None:
            self.color = color
        text_color = ''
        if not no_color and self.color is not None:
            text_color = 'text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="{text_color} material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{text_color} {self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'{self.icon_svg}'
        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''

    def get_icon_tag_pure(self, icon_style='', color=None, no_color=False):

        if color is not None:
            self.color = color
        text_color = ''
        if not no_color and self.color is not None:
            text_color = 'text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''

    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("Icons")

    def __str__(self):
        return self.title


class Download(Icon):
    page = models.ForeignKey("core.page", verbose_name=_(
        "page"), on_delete=models.CASCADE)
    
    file = models.FileField(_("فایل ضمیمه"), null=True, blank=True,
                            upload_to=APP_NAME+'/downloads', storage=upload_storage, max_length=100)
    mirror_link = models.CharField(
        _('آدرس بیرونی'), null=True, blank=True, max_length=10000)
    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("اصلاح شده در"), auto_now_add=False, auto_now=True)
    download_counter = models.IntegerField(_("download_counter"), default=0)
    persons = models.ManyToManyField(
        "authentication.person", blank=True, related_name="person_downloads", verbose_name=_("persons"))
    is_open = models.BooleanField(_("is_open?"), default=False)
    person = models.ForeignKey("authentication.person", null=True,
                                blank=True, verbose_name=_("person"), on_delete=models.CASCADE)
    class_name='download'
    app_name=APP_NAME
    @property
    def get_download_url(self):
        if self.mirror_link and self.mirror_link is not None:
            return self.mirror_link
        if self.file:
            ss= reverse(APP_NAME+':download', kwargs={'pk': self.pk})
            return ss
        else:
            return ''

    @property
    def get_full_download_url(self):
        if self.mirror_link and self.mirror_link is not None:
            return self.mirror_link
        if self.file:
            ss= reverse(APP_NAME+':download', kwargs={'pk': self.pk})
            return FULL_SITE_URL[0:len(FULL_SITE_URL)-1]+ss
        else:
            return ''

          

    class Meta:
        verbose_name = _("Download")
        verbose_name_plural = _("Downloads")

    def __str__(self):
        return f'{self.page} {self.title}'


    def get_qrcode_url(self):
        if self.pk is None:
            super(Download,self).save()
        import os
        file_path = QRCODE_ROOT
        file_name=self.class_name+str(self.pk)+".svg"
        file_address=os.path.join(QRCODE_ROOT,file_name)
        if not os.path.exists(file_address):
            content=self.get_full_download_url
            generate_qrcode(content=content,file_name=file_name,file_address=file_address,file_path=file_path,)
        return f"{QRCODE_URL}{file_name}"
 

class Link(Icon,LinkHelper):
    page = models.ForeignKey("core.page", verbose_name=_(
        "page"),null=True,blank=True, on_delete=models.CASCADE)
    
    url = models.CharField(_("url"), max_length=2000)
    new_tab=models.BooleanField(_("new_tab"),default=False)
    person = models.ForeignKey("authentication.person", null=True,
                                blank=True, verbose_name=_("person"), on_delete=models.CASCADE)
    class_name='link'
    app_name=APP_NAME
    def __str__(self):
        return f'{self.page} {self.title}'

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def get_absolute_url(self):
        return reverse("Link_detail", kwargs={"pk": self.pk})

    def get_link_btn(self):
        target='target="_blank"' if self.new_tab else ''
        return f"""

            <a {target} class="btn btn-{self.color} " href="{self.url}">
            <span class="ml-2">
            {self.get_icon_tag_pure()}
            </span>
            {self.title}
            </a>
        """
    
    def get_qrcode_url(self):
        if self.pk is None:
            super(Link,self).save()
        import os
        file_path = QRCODE_ROOT
        file_name=self.class_name+str(self.pk)+".svg"
        file_address=os.path.join(QRCODE_ROOT,file_name)
        if not os.path.exists(file_address):
            content=self.url
            generate_qrcode(content=content,file_name=file_name,file_address=file_address,file_path=file_path,)
        return f"{QRCODE_URL}{file_name}"
  

class Image(models.Model,LinkHelper,DateTimeHelper):
    page=models.ForeignKey("core.page", verbose_name=_("page"), on_delete=models.CASCADE)
    app_name=APP_NAME
    class_name='image'

    title = models.CharField(_("title"), max_length=50)
    description = HTMLField(_("توضیحات"), null=True,
                            blank=True, max_length=50000)
    priority = models.IntegerField(_("priority"), default=1000)

    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'ImageBase/Thumbnail/',
                                         null=True, blank=True, height_field=None, width_field=None, max_length=None)
    image_main_origin = models.ImageField(_("تصویر اصلی"), null=True, blank=True, upload_to=IMAGE_FOLDER +
                                          'ImageBase/Main/', height_field=None, width_field=None, max_length=None)
    image_header_origin = models.ImageField(_("تصویر سربرگ"), null=True, blank=True, upload_to=IMAGE_FOLDER +
                                            'ImageBase/Header/', height_field=None, width_field=None, max_length=None)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    creator=models.ForeignKey("authentication.person", verbose_name=_("person"),null=True,blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.page} {self.title}'
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("تصاویر")
    def get_download_url(self): 
        if self.image_main_origin:
            return reverse(APP_NAME+':image_download', kwargs={'pk': self.pk})
        else:
            return ''

    def download_response(self):
        #STATIC_ROOT2 = os.path.join(BASE_DIR, STATIC_ROOT)
        file_path = str(self.image_main_origin.path)
        # return JsonResponse({'download:':str(file_path)})
        import os
        from django.http import HttpResponse
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                return response
        from log.repo import LogRepo
        LogRepo().add_log(title="Http404 core models", app_name=APP_NAME)
        raise Http404



    @property
    def image(self):
        if self.image_main_origin:
            return MEDIA_URL+str(self.image_main_origin)

    @property
    def thumbnail(self):
        return self.get_or_create_thumbnail()
         

    def get_or_create_thumbnail(self, *args, **kwargs):
        if self.thumbnail_origin:
            return MEDIA_URL+str(self.thumbnail_origin)
        try:
            if self.image_main_origin is None:
                return f'{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png'
        except:
            return f'{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png'
        # Opening the uploaded image

        from PIL import Image as PilImage
        from io import BytesIO
        import sys
        from django.core.files.uploadedfile import InMemoryUploadedFile
        try:
            image = PilImage.open(self.image_main_origin)
        except:
            return None
        width11, height11 = image.size
        ratio11 = float(height11)/float(width11)
     

        output = BytesIO()
        from utility.repo import ParameterRepo,Parameter
        THUMBNAIL_DIMENSION=150
        parameter=Parameter.objects.filter(app_name=APP_NAME).filter(name=ParameterNameEnum.THUMBNAIL_DIMENSION).first()
        if parameter is not None:

            THUMBNAIL_DIMENSION =parameter.value
         
        # try:
        #     a = THUMBNAIL_DIMENSION+100
        # except:
        #     THUMBNAIL_DIMENSION = 250
        # Resize/modify the image
        image = image.resize((THUMBNAIL_DIMENSION, int(ratio11*float(THUMBNAIL_DIMENSION))), PilImage.Resampling.LANCZOS)
        try:
        # after modifications, save it to the output
            image.save(output, format='JPEG', quality=95)
   
            output.seek(0)

            # change the imagefield value to be the newley modifed image value
            image_name = f"{self.image_main_origin.name.split('.')[0]}.jpg"
            image_path = IMAGE_FOLDER+'ImageBase/Thumbnail'
            self.thumbnail_origin = InMemoryUploadedFile(output, 'ImageField', image_name, image_path, sys.getsizeof(output), None)
        
            self.save()
            # return MEDIA_URL+str(self.image_main_origin)
            return MEDIA_URL+str(self.thumbnail_origin)
        except:
            return self.image


class Tag(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)  
    pages=models.ManyToManyField("core.page",blank=True, verbose_name=_("pages"))
    class_name='tag'
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.title 
    

class Location(models.Model,LinkHelper):
    title = models.CharField(
        _("عنوان نقطه"), max_length=100)
    location = models.CharField(_("لوکیشن"), max_length=1000)
    latitude=models.CharField(_("latitude"),null=True,blank=True, max_length=50)
    longitude=models.CharField(_("longitude"),null=True,blank=True, max_length=50)


    creator = models.ForeignKey("authentication.person", null=True,blank=True,related_name="maplocation_set", verbose_name=_("person"), on_delete=models.CASCADE)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    class_name = "location"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("لوکیشن")
        verbose_name_plural = _("لوکیشن ها")

    def __str__(self):
        return f'{self.title}'

    
    def save(self, *args, **kwargs):
        (result,message,location)=FAILED,'',None
        if self.location is not None:
            self.location = self.location.replace('width="600"', 'width="100%"')
            self.location = self.location.replace('height="450"', 'height="400"')
        super(Location, self).save(*args, **kwargs)
        if self.id is not None:
            location=self
            result=SUCCEED
            message='موقعیت با موفقیت اضافه شد.'
        return result,message,location
 

 
    def get_link_to_map(self):
        return f'https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}'
    def get_link_to_map_tag(self):
        return f"""
            <a title="نمایش روی نقشه" target="_blank" href="{self.get_link_to_map()}">
                <span class="material-icons">
                    location_on
                    </span>
                
            </a>
        """
 
 
class Area(models.Model,LinkHelper):
    page=models.ForeignKey("core.page", verbose_name=_("page"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    code=models.CharField(_("code"), max_length=50)
    area = models.CharField(_("area"),blank=True,null=True, max_length=1000)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    app_name=APP_NAME
    class_name="area"
    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if self.area is not None:
            self.area = self.area.replace('width="600"', 'width="100%"')
            self.area = self.area.replace('height="450"', 'height="400"')
        super(Area, self).save(*args, **kwargs)

 