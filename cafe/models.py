from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from phoenix.server_settings import CURRENCY
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice
from market.models import Customer
from core.models import Page as CorePage,DateTimeHelper,Event
from market.models import Supplier
from market.models import CartItem
from organization.models import OrganizationalUnit,Employee
from .enums import OrderStatusEnum,get_table_status_color


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
    @property
    def status(self):
        current_order=Order.objects.exclude(status=OrderStatusEnum.FINISHED).filter(table_id=self.pk).last()
        if current_order is not None:
            return current_order.status
        return OrderStatusEnum.FREE
 
    def color(self):
        return get_table_status_color(self.status)


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
          

class Barista(Employee):
    
    class_name="barista"
    app_name=APP_NAME


    class Meta:
        verbose_name = _("Barista")
        verbose_name_plural = _("Baristas")
 
 
    def save(self):
        (result,message,employee)=FAILED,'',self
        super(Employee,self).save()
        result=SUCCEED
        message='کارمند جدید با موفقیت اضافه شد.'
        return (result,message,employee)


class Order(models.Model,LinkHelper):
    invoices=models.ManyToManyField("accounting.invoice",blank=True, verbose_name=_("invoices"))
    table=models.ForeignKey("table", verbose_name=_("table"), on_delete=models.CASCADE)
    customer=models.ForeignKey("market.customer", verbose_name=_("customer"), on_delete=models.CASCADE)
    status=models.CharField(_("status"),choices=OrderStatusEnum.choices, max_length=50)

    class_name="order"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f'{self.table} {self.status}'

 

class OrderLog(Event):
    order=models.ForeignKey("order", verbose_name=_("order"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("OrderLog")
        verbose_name_plural = _("OrderLogs")
 