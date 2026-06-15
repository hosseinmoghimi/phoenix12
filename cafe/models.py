from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice
from market.models import Customer
from core.models import Page as CorePage
from market.models import Supplier
from market.models import CartItem
 
class Table(models.Model,LinkHelper):
    class_name="table"
    app_name=APP_NAME
    title=models.CharField(_("عنوان"), max_length=50)
    table_no=models.IntegerField(_("شماره میز"), default=0)
    supplier=models.ForeignKey("market.supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    code=models.CharField(_("کد"), max_length=500)
    capacity=models.IntegerField(_("ظرفیت"),default=4)

    class Meta:
        verbose_name = _("Table")
        verbose_name_plural = _("Tables")

    def __str__(self):
        return self.title
 
    def save(self):
        (result,message,table)=FAILED,'',self
         
        super(Table,self).save()   
        result=SUCCEED
        message="میز با موفقیت اضافه شد."
        return (result,message,table)

 
class Menu(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    shops=models.ManyToManyField("market.shop", verbose_name=_("shops"),blank=True)
    
    def __str__(self):
        return self.title
    
    class_name="menu"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")
    def save(self):
        (result,message,menu)=FAILED,'',self
        
        super(Menu,self).save()   
        result=SUCCEED
        message="منو با موفقیت اضافه شد."
        return (result,message,menu)
          