from resume.enums import *
from tinymce.models import HTMLField
from phoenix.server_settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.db import models
from resume.apps import APP_NAME
from django.utils.translation import gettext as _

from utility.models import LinkHelper
IMAGE_FOLDER=APP_NAME+"/img/"
from core.models import Page
from django.shortcuts import reverse



class ResumePage(Page):
    def save(self,*args, **kwargs):
        self.app_name=APP_NAME
        return super(ResumePage,self).save(*args, **kwargs)




class ResumeCategory(models.Model,LinkHelper):
    resume_index=models.ForeignKey("resumeindex", verbose_name=_("resume"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    class_name="resumecategory"
    app_name=APP_NAME
    def __str__(self):
        return f"""{self.resume_index}  {self.title} """

    class Meta:
        verbose_name = _("ResumeCategory")
        verbose_name_plural = _("ResumeCategorys")

    def save(self,*args, **kwargs):
        self.class_name="resumecategory"
        return super(ResumeCategory,self).save(*args, **kwargs)

 
class Resume(ResumePage,LinkHelper):
    category=models.ForeignKey("resumecategory", verbose_name=_("category"), on_delete=models.CASCADE)
    start_date=models.DateField(_("start_date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    end_date=models.DateField(_("end_date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    location=models.CharField(_("location"),null=True,blank=True, max_length=50)
    class_name="resume"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Resume")
        verbose_name_plural = _("Resumes")


    def save(self,*args, **kwargs):
        self.class_name="resume"
        return super(Resume,self).save(*args, **kwargs)

class ResumeIndex(models.Model,LinkHelper):
    class_name="resumeindex"
    app_name=APP_NAME
    language=models.CharField(_("language"),choices=LanguageEnum.choices,default=LanguageEnum.ENGLISH, max_length=50)
    image_header_origin =models.ImageField(_("تصویر سربرگ"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Resume/Header/', height_field=None, width_field=None, max_length=None)                              
  
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    title=models.CharField(_("title"),null=True,blank=True, max_length=100)
    typing_text=models.CharField(_("typing_text"), null=True,blank=True,default="Developer,Designer,Programmer",max_length=500)
    about_top=HTMLField(_("about_top"),null=True,blank=True)
    image_main_origin = models.ImageField(_("تصویر اصلی"),null=True, blank=True, upload_to=IMAGE_FOLDER +
                                     'Resume/Main/', height_field=None, width_field=None, max_length=None)
    job_title=models.CharField(_("job_title"),null=True,blank=True, max_length=300)
    about_middle=HTMLField(_("about_middle"),null=True,blank=True)

    birth_day=models.DateField(_("birth_day"),null=True,blank=True, auto_now=False, auto_now_add=False)
    website=models.CharField(_("website"),null=True,blank=True, max_length=500)
    # phone=models.CharField(_("phone"),null=True,blank=True, max_length=50)
    # address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    city=models.CharField(_("city"),null=True,blank=True, max_length=50)
    age=models.IntegerField(_("age"),null=True,blank=True)
    degree=models.CharField(_("degree"),null=True,blank=True, max_length=100)
    email=models.CharField(_("email"),null=True,blank=True, max_length=100)
    freelance=models.CharField(_("freelance"),null=True,blank=True, max_length=100)
    about_bottom=HTMLField(_("about_bottom"),null=True,blank=True)



    facts_top=HTMLField(_("facts_top"),null=True,blank=True)
    skills_top=HTMLField(_("skills_top"),null=True,blank=True)
    resume_top=HTMLField(_("resume_top"),null=True,blank=True)
    portfolio_top=HTMLField(_("portfolio_top"),null=True,blank=True)
    services_top=HTMLField(_("services_top"),null=True,blank=True)

    location=models.CharField(_("location"),null=True,blank=True, max_length=200)
    call=models.CharField(_("call"),null=True,blank=True, max_length=50)

    def get_qrcode_url(self):
        from phoenix.settings import QRCODE_ROOT,FULL_SITE_URL,QRCODE_URL
        from utility.qrcode import generate_qrcode
        
        if self.pk is None:
            super(ResumeIndex,self).save()
        import os
        file_path = QRCODE_ROOT
        file_name=APP_NAME+"_"+self.class_name+str(self.pk)+".svg"
        # file_address=os.path.join(file_path,file_name)
        file_address=os.path.join(QRCODE_ROOT,file_name)
        content=FULL_SITE_URL[0:len(FULL_SITE_URL)-1]+self.get_absolute_url()
        generate_qrcode(content=content,file_name=file_name,file_address=file_address,file_path=file_path)

        file_name=APP_NAME+"_"+self.class_name+str(self.pk)+".svg"   
        return f"{QRCODE_URL}{file_name}"

    def get_print_url(self):
        return reverse(APP_NAME+":resume_print",kwargs={'pk':self.pk})
    class Meta:
        verbose_name = _("ResumeIndex")
        verbose_name_plural = _("ResumeIndexs")

    def __str__(self):
        return self.language+" : "+(self.person.full_name if self.title is None else self.title)

    def image(self):
        if self.image_main_origin:
            return MEDIA_URL+str(self.image_main_origin)
        else:

            from .views import TEMPLATE_ROOT,LanguageCode
            TEMPLATE_ROOT=TEMPLATE_ROOT+LanguageCode(self.language)+"/"
            return f'{STATIC_URL}{TEMPLATE_ROOT}/img/profile-img.jpg'
    def image_header(self):
        if self.image_header_origin:
            return MEDIA_URL+str(self.image_header_origin)
        else:
            from .views import TEMPLATE_ROOT,LanguageCode
            TEMPLATE_ROOT=TEMPLATE_ROOT+LanguageCode(self.language)+"/"
            return f'{STATIC_URL}{TEMPLATE_ROOT}/img/hero-bg.jpg'
    
    # def get_absolute_url(self):
        
    #     return reverse(APP_NAME+":resume_index", kwargs={"pk": self.pk})
    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="edit" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """

    # def get_edit_url(self):
    #     return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'

class ResumeService(ResumePage):
    resume_index=models.ForeignKey("resumeindex", verbose_name=_("resume"), on_delete=models.CASCADE)
    # color=models.CharField(_("color"),choices=ServiceColorEnum.choices,default=ServiceColorEnum.blue, max_length=50)
    # class_name="resumeservice"

    class Meta:
        verbose_name = _("ResumeService")
        verbose_name_plural = _("ResumeServices")

    def save(self,*args, **kwargs):
        self.class_name="resumeservice"
        return super(ResumeService,self).save(*args, **kwargs)

class ResumePortfolio(ResumePage):
    resume_index=models.ForeignKey("resumeindex", verbose_name=_("resume"), on_delete=models.CASCADE)
    filter=models.CharField(_("filter"),choices=FilterEnum.choices,default=FilterEnum.web, max_length=50)
    # image_main_origin =models.ImageField(_("تصویر سربرگ"), upload_to=IMAGE_FOLDER +
    #                                  'Resume/Portfolio/', height_field=None, width_field=None, max_length=None)                              
    category=models.CharField(_("category"), max_length=500)
    # priority=models.IntegerField(_("priority"),default=100)
    # def image(self):
    #     if self.image_main_origin:
    #         return MEDIA_URL+str(self.image_main_origin)
    

    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")

    def save(self,*args, **kwargs):
        self.class_name="resumeportfolio"
        return super(ResumePortfolio,self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse(APP_NAME+":portfolio",kwargs={'pk':self.pk})
class ResumeSkill(models.Model):
    resume_index=models.ForeignKey("resumeindex", verbose_name=_("resume"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    percentage=models.IntegerField(_("percentage"),default=10)
    priority=models.IntegerField(_("priority"),default=10)
    class_name="resumeskill"
    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="edit" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'


    class Meta:
        verbose_name = _("ResumeSkill")
        verbose_name_plural = _("ResumeSkills")

    def __str__(self):
        return f"""{self.resume_index.person.full_name} : {self.title} : {self.percentage}"""

  
    def get_absolute_url(self):
        return reverse(f"{APP_NAME}:{self.class_name}", kwargs={"pk": self.pk})


class ResumeFact(models.Model):
    resume_index=models.ForeignKey("resumeindex", verbose_name=_("resume"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=500)
    color=models.CharField(_("color"),null=True,blank=True, max_length=50)
    priority=models.IntegerField(_("priority"),default=10)
    icon=models.CharField(_("icon"),choices=IconEnum.choices,null=True,blank=True, max_length=100)
    count=models.IntegerField(_("count"),default=10)
    class_name="resumefact"
    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="edit" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """
    def get_icon_tag(self):
        return f"""
        <i class="bi bi-emoji-smile"></i>
        """
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'

    

    class Meta:
        verbose_name = _("ResumeFact")
        verbose_name_plural = _("ResumeFacts")

    def __str__(self):
        return f"""{self.resume_index.person.full_name} : {self.title} : {self.count}"""

    def get_absolute_url(self):
        return reverse(f"{APP_NAME}:{self.class_name}", kwargs={"pk": self.pk})



class ResumeTestimonial(models.Model):
    resume_index=models.ForeignKey("resumeindex", verbose_name=_("resume"), on_delete=models.CASCADE)
    teller = models.CharField(_("teller"), max_length=2000)
    teller_description = models.CharField(_("teller_description"), max_length=2000)
    title = models.CharField(_("عنوان"), max_length=2000)
    body = models.CharField(_("متن"), max_length=2000, null=True, blank=True)
    footer = models.CharField(_("پانوشت"), max_length=200)
    priority = models.IntegerField(_("ترتیب"), default=100)
    date_added=models.DateField(_("date_added"), auto_now=False, auto_now_add=False)
    image_origin = models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'Testimonial/',
                                     null=True, blank=True, height_field=None, width_field=None, max_length=None)
    class_name="resumetestimonial"
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
    
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("Testimonial")

    def save(self,*args, **kwargs):
        return super(ResumeTestimonial,self).save(*args, **kwargs)



    def get_edit_btn(self):
        return f"""
          <a target="_blank" title="edit" href="{self.get_edit_url()}">
            <i class="material-icons">
                edit
            </i>
        </a>
        """

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'




class ContactMessage(models.Model):
    resume_index=models.ForeignKey("resumeindex", verbose_name=_("resume"), on_delete=models.CASCADE)
    full_name = models.CharField(_("نام کامل"), max_length=50)
    mobile = models.CharField(_("شماره تماس"), max_length=50)
    email = models.EmailField(_("ایمیل"), max_length=254)
    subject = models.CharField(_("عنوان پیام"), max_length=50)
    message = models.CharField(_("متن پیام"), max_length=50)
    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    app_name = APP_NAME
    class_name="contactmessage"

    class Meta:
        verbose_name = _("ContactMessage")
        verbose_name_plural = _("پیام های ارتباط با ما")

    def __str__(self):
        return f"""{self.resume_index.person.full_name} : @{self.full_name}"""


class ResumeSocialLink(models.Model):
    resume_index=models.ForeignKey("resumeindex", verbose_name=_("resumeindex"), on_delete=models.CASCADE)
    title=models.CharField(_("title"),choices=LinkClassEnum.choices, max_length=50)
    href=models.CharField(_("href"), max_length=5000)
    link_class=models.CharField(_("link_class"),choices=LinkClassEnum.choices, max_length=50)
    icon=models.CharField(_("icon"),choices=IconEnum.choices, max_length=50)
    class_name="resumesociallink"
    
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    class Meta:
        verbose_name = _("ResumeSocialLink")
        verbose_name_plural = _("ResumeSocialLinks")

    def __str__(self):
        return f"""{self.resume_index.title} : {self.title}"""

    def get_absolute_url(self):
        return reverse("ResumeSocialLink_detail", kwargs={"pk": self.pk})
