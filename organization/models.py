from django.db import models
from core.models import Page,LinkHelper,FAILED,SUCCEED,reverse
from phoenix.server_settings import STATIC_URL,MEDIA_URL
from django.utils.translation import gettext as _
from .apps import APP_NAME
from utility.models import DateTimeHelper


class OrganizationalUnit(Page,LinkHelper):
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person account"), on_delete=models.CASCADE)
    # account_code=models.CharField(_("account_code"), max_length=50)
    @property
    def account(self):
        return self.person_account
    #     from accounting.models import Account
    #     return Account.objects.filter(code=self.account_code).first()

    class Meta:
        verbose_name = _("OrganizationalUnit")
        verbose_name_plural = _("OrganizationalUnits")
 
    def save(self):
        (result,message,organizational_unit)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="organizationalunit"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(OrganizationalUnit,self).save()
        result=SUCCEED
        message="سازمان با موفقیت اضافه شد."
        return (result,message,organizational_unit)
    
    def get_tree_chart_url(self):
        return reverse(APP_NAME+':tree_chart',kwargs={'pk':self.pk})
    
    @property
    def children(self):
        return OrganizationalUnit.objects.filter(parent_id=self.id)
    
    def all_sub_organizational_units(self):
        ids=[]
        for organizational_unit in self.children.all():
            ids.append(organizational_unit.id)
            for i in organizational_unit.all_sub_organizational_units():
                ids.append(i.id)
        return OrganizationalUnit.objects.filter(id__in=ids)
    

    @property
    def thumbnail(self):
        if self.thumbnail_origin is not None and not self.thumbnail_origin=='':
            return f"{MEDIA_URL}{self.thumbnail_origin}"
          
        if self.person_account.thumbnail_origin is not None and not self.person_account.thumbnail_origin=='':
            return self.person_account.thumbnail
        
        if self.person_account.person.image_origin is not None and not self.person_account.person.image_origin=='':
            return self.person_account.person.image
        
        try:
            return f"{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png/"
        except:
            pass 


class Employee(models.Model,LinkHelper,DateTimeHelper):
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person account"), on_delete=models.CASCADE)
    organizational_unit=models.ForeignKey("organizationalunit",null=True,blank=True, verbose_name=_("organizational_unit"), on_delete=models.CASCADE)
    job_title=models.CharField(_("job_title"),max_length=100)

    class_name="employee"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"{self.person_account}  {self.job_title}  {self.organizational_unit}"
 
 
    def save(self):
        (result,message,employee)=FAILED,'',self
        super(Employee,self).save()
        result=SUCCEED
        message='کارمند جدید با موفقیت اضافه شد.'
        return (result,message,employee)