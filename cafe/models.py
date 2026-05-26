from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice
from market.models import Customer
from core.models import Page as CorePage
from market.models import Supplier
 
class Table(models.Model,LinkHelper):
    class_name="table"
    app_name=APP_NAME
    title=models.CharField(_("عنوان"), max_length=50)
    table_no=models.IntegerField(_("شماره میز"), default=0)
    supplier=models.ForeignKey("market.supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("Table")
        verbose_name_plural = _("Tables")

    def __str__(self):
        return self.title
   
    class Meta:
        verbose_name = _("MealItem")
        verbose_name_plural = _("MealItems")
 
    def save(self):
        (result,message,table)=FAILED,'',self
         
        super(Table,self).save()   
        result=SUCCEED
        message="میز با موفقیت اضافه شد."
        return (result,message,table)

 
class Menu(CorePage):
    supplier=models.ForeignKey("market.supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    # title=models.CharField(_("title"), max_length=50)
    shops=models.ManyToManyField("market.shop", verbose_name=_("shops"),blank=True)
    

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")
    def save(self):
        (result,message,menu)=FAILED,'',self
        if self.class_name is None or self.class_name=="":
            self.class_name="menu"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Menu,self).save()   
        result=SUCCEED
        message="آیتم غذایی با موفقیت اضافه شد."
        return (result,message,menu)
         
  

class TableCustomer(Customer):
    table=models.ForeignKey("cafe.table", verbose_name=_("table"), on_delete=models.CASCADE)
    class_name="tablecustomer"

    class Meta:
        verbose_name = _("TableCustomer")
        verbose_name_plural = _("TableCustomers")  


class MenuItem(models.Model):
    shop=models.ForeignKey("market.shop", verbose_name=_("shop"), on_delete=models.CASCADE)
    in_cart=models.IntegerField(_("in_cart"),default=0)

     
    class Meta:
        verbose_name = _("MenuItem")
        verbose_name_plural = _("MenuItems")  


