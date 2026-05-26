from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED,ImageHelper
from phoenix.server_settings import CURRENCY,MEDIA_URL
from .apps import APP_NAME
from accounting.models import Product,InvoiceLine,Invoice,CorePage
from .enums import *
from utility.enums import * 
from utility.log import leolog
IMAGE_FOLDER = APP_NAME+"/images/"

class WareHouse(models.Model,LinkHelper,ImageHelper):
    name=models.CharField(_("نام"), max_length=50)
    thumbnail_origin=models.ImageField(_("thumbnail"),blank=True,null=True, upload_to=IMAGE_FOLDER+"warehouse", height_field=None, width_field=None, max_length=None)
    person_account=models.ForeignKey("accounting.personaccount", verbose_name=_("person_account"),null=True,blank=True, on_delete=models.PROTECT)
    employees=models.ManyToManyField("organization.employee",blank=True, verbose_name=_("employees"))
    app_name=APP_NAME
    class_name="warehouse"
    class Meta:
        verbose_name = _("WareHouse")
        verbose_name_plural = _("WareHouses")

    def __str__(self):
        return self.name
 

    def save(self):
         (result,message,warehouse)=FAILED,'',self
         super(WareHouse,self).save()
         result=SUCCEED
         message='انبار با موفقیت اضافه شد.'
         return  (result,message,warehouse)
 
 
class MaterialPort(models.Model,LinkHelper,DateTimeHelper):
    person=models.ForeignKey("authentication.person", verbose_name=_("person"), on_delete=models.CASCADE)
    source=models.ForeignKey("warehouse",related_name="material_from", verbose_name=_("source"), on_delete=models.PROTECT)
    destination=models.ForeignKey("warehouse",related_name="material_to", verbose_name=_("destination"), on_delete=models.PROTECT)
    product=models.ForeignKey("accounting.product", verbose_name=_("product"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    quantity=models.IntegerField(_("quantity"),default=1)
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD,max_length=100)
    class_name="materialport"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("MaterialPort")
        verbose_name_plural = _("MaterialPorts")

    def __str__(self):
        return f"{self.person}  {self.product}  {self.direction}"


class WareHouseSheet(models.Model,LinkHelper,DateTimeHelper):
    warehouse=models.ForeignKey("warehouse", verbose_name=_("warehouse"),null=True,blank=True, on_delete=models.PROTECT)
    organizational_unit=models.ForeignKey("organization.organizationalunit",null=True,blank=True, verbose_name=_("organizational_unit"), on_delete=models.PROTECT)
    invoice_line=models.ForeignKey("accounting.invoiceline", verbose_name=_("invoice_line"), on_delete=models.PROTECT)
    direction=models.CharField(_("direction"),max_length=50,choices=WareHouseSheetDirectionEnum.choices)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    employee=models.ForeignKey("organization.employee", verbose_name=_("employee"), on_delete=models.PROTECT)
    shelf=models.CharField(_("shelf"),null=True,blank=True,max_length=50)
    row=models.CharField(_("row"),null=True,blank=True,max_length=50)
    col=models.CharField(_("col"),null=True,blank=True,max_length=50)
    description=models.CharField(_("description"),null=True,blank=True,max_length=500)
    status=models.CharField(_("status"),choices=SignatureStatusEnum.choices,default=SignatureStatusEnum.REQUESTED, max_length=50)
    type=models.CharField(_("type"),choices=WareHouseSheetTypeEnum.choices,default=WareHouseSheetTypeEnum.MISC, max_length=50)
    class_name="warehousesheet"
    app_name=APP_NAME
    @property
    def status_color(self):
        if self.status==SignatureStatusEnum.REVIEWED:
            return 'primary'
        if self.status==SignatureStatusEnum.CONFIRMED:
            return 'success'
        if self.status==SignatureStatusEnum.DENIED:
            return 'danger'
        if self.status==SignatureStatusEnum.REQUESTED:
            return 'secondary'
    class Meta:
        verbose_name = _("WareHouseSheet")
        verbose_name_plural = _("WareHouseSheets")
    @property
    def sum(self):
        return self.invoice_line.line_total
    # @property
    # def status(self):
    #     signature=WareHouseSheetSignature.objects.filter(warehouse_sheet_id=self.id).last()
    #     return signature
    def __str__(self):
        return f"{self.warehouse} - {self.invoice_line.invoice_line_item} - {self.invoice_line.quantity} {self.invoice_line.unit_name} - {self.direction}     "

    def balance(self):
        if self.direction==WareHouseSheetDirectionEnum.IN:
            return self.quantity
        if self.direction==WareHouseSheetDirectionEnum.OUT:
            return 0-self.quantity
  
    def save(self):
        super(WareHouseSheet,self).save() 
        ProductInWareHouse.normalize_products_in_warehouse(warehouse_id=self.warehouse.id,product_id=self.invoice_line.invoice_line_item.id,unit_name=self.invoice_line.unit_name)
    
    def delete(self):
        super(WareHouseSheet,self).delete()
        ProductInWareHouse.normalize_products_in_warehouse(warehouse_id=self.warehouse.id,product_id=self.invoice_line.invoice_line_item.id,unit_name=self.invoice_line.unit_name)
    
class WareHouseSheetSignature(models.Model,LinkHelper,DateTimeHelper):
    warehouse_sheet=models.ForeignKey("warehousesheet", verbose_name=_("warehouse_sheet"), on_delete=models.PROTECT)
    employee=models.ForeignKey("organization.employee", verbose_name=_("employee"), on_delete=models.PROTECT)
    status=models.CharField(_("status"),choices=SignatureStatusEnum.choices, max_length=50)
    description=models.CharField(_("description"),null=True,blank=True, max_length=50)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    class_name='warehousesheetsignature'
    app_name=APP_NAME
    
    @property
    def status_color(self):
        if self.status==SignatureStatusEnum.REVIEWED:
            return 'primary'
        if self.status==SignatureStatusEnum.CONFIRMED:
            return 'success'
        if self.status==SignatureStatusEnum.DENIED:
            return 'danger'
        if self.status==SignatureStatusEnum.REQUESTED:
            return 'secondary'
        
    class Meta:
        verbose_name = _("WareHouseSheetSignature")
        verbose_name_plural = _("WareHouseSheetSignatures")

    def __str__(self):
        return f'{self.employee}  {self.status}  {self.warehouse_sheet}'
 
    def save(self):
        self.warehouse_sheet.status=self.status
        self.warehouse_sheet.save()
        return super(WareHouseSheetSignature,self).save()


class WareHouseSheetLabel(models.Model,LinkHelper,DateTimeHelper):
    warehouse_sheet=models.ForeignKey("warehousesheet", verbose_name=_("warehouse_sheet"), on_delete=models.PROTECT)
    serial_no=models.CharField(_("serial_no"),null=True,blank=True, max_length=50)
    lot_no=models.CharField(_("lot_no"),null=True,blank=True, max_length=50)
    lot_no=models.CharField(_("lot_no"),null=True,blank=True, max_length=50)
    barcode_1=models.CharField(_("barcode_1"),null=True,blank=True, max_length=50)
    barcode_2=models.CharField(_("barcode_2"),null=True,blank=True, max_length=50)
    barcode_3=models.CharField(_("barcode_3"),null=True,blank=True, max_length=50)
    label_origin=models.ImageField(_("label_origin"),blank=True,null=True, upload_to=IMAGE_FOLDER+"label", height_field=None, width_field=None, max_length=None)
    production_date=models.DateTimeField(_("production_date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    expiration_date=models.DateTimeField(_("expiration_date"),null=True,blank=True, auto_now=False, auto_now_add=False)
    description=models.CharField(_("description"),null=True,blank=True, max_length=50)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    class_name='warehousesheetlabel'
    app_name=APP_NAME
    class Meta:
        verbose_name = _("WareHouseSheetLabel")
        verbose_name_plural = _("WareHouseSheetLabels")

    def __str__(self):
        return f'{self.warehouse_sheet}'
    @property
    def label(self):
          
        if self.label_origin is None or str(self.label_origin)=="":
            return None
        else:
            return f"{MEDIA_URL}{self.label_origin}"


class MaterialRequest(models.Model):
    invoice=models.ForeignKey("accounting.invoice", verbose_name=_("invoice"), on_delete=models.PROTECT)
    product=models.ForeignKey("accounting.product", verbose_name=_("product"), on_delete=models.PROTECT)
    quantity=models.FloatField(_("quantity"))
    unit_name=models.CharField(_("unit_name"), max_length=50)
    unit_price=models.IntegerField(_("unit_price"))
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    warehouse=models.ForeignKey("warehouse", verbose_name=_("warehouse"),null=True,blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("MaterialRequest")
        verbose_name_plural = _("MaterialRequests")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("MaterialRequest_detail", kwargs={"pk": self.pk})


class ProductInWareHouse(models.Model):
    product=models.ForeignKey("accounting.product", verbose_name=_("product"), on_delete=models.PROTECT)
    warehouse=models.ForeignKey("warehouse", verbose_name=_("warehouse"),null=True,blank=True, on_delete=models.CASCADE)
    unit_name=models.CharField(_("unit_name"), max_length=50)
    quantity=models.FloatField(_("quantity"))

               
    def normalize_products_in_warehouse(*args,**kwargs):
        result,message,product_in_warehouse=FAILED,"",None
        # if not self.request.user.has_perm(APP_NAME+".delete_productinwarehouse"):
        #     message='دسترسی شما برای این فرآیند مجاز نمی باشد.'
        #     return FAILED,message,None
        
        list1=ProductInWareHouse.objects.all()

        if 'unit_name' in kwargs and kwargs['unit_name'] is not None and len(kwargs['unit_name'])>0:
            list1=list1.filter(unit_name=kwargs['unit_name'])
       
        if 'product_id' in kwargs and kwargs['product_id'] is not None and kwargs['product_id']>0:
            list1=list1.filter(product_id=kwargs['product_id'])
       
        if 'warehouse_id' in kwargs and kwargs['warehouse_id'] is not None and kwargs['warehouse_id']>0:
            list1=list1.filter(warehouse_id=kwargs['warehouse_id'])
        list1.delete()

        warehouse_sheets=WareHouseSheet.objects.filter(status=SignatureStatusEnum.CONFIRMED)
        
        if 'product_id' in kwargs and kwargs['product_id'] is not None and kwargs['product_id']>0:
            warehouse_sheets=warehouse_sheets.filter(invoice_line__invoice_line_item_id=kwargs['product_id'])
        if 'warehouse_id' in kwargs and kwargs['warehouse_id'] is not None and kwargs['warehouse_id']>0:
            warehouse_sheets=warehouse_sheets.filter(warehouse_id=kwargs['warehouse_id'])
        if 'unit_name' in kwargs and kwargs['unit_name'] is not None and len(kwargs['unit_name'])>0:
            warehouse_sheets=warehouse_sheets.filter(invoice_line__unit_name=kwargs['unit_name'])

        for warehouse_sheet in warehouse_sheets:
            product_in_warehouse=ProductInWareHouse.objects.filter(warehouse_id=warehouse_sheet.warehouse.id).filter(product_id=warehouse_sheet.invoice_line.invoice_line_item.id).filter(unit_name=warehouse_sheet.invoice_line.unit_name).first()
            if product_in_warehouse is None:
                product_in_warehouse=ProductInWareHouse()
                quantity=warehouse_sheet.invoice_line.quantity
                if warehouse_sheet.direction==WareHouseSheetDirectionEnum.OUT:
                    quantity=0-quantity
                product_in_warehouse.product_id=warehouse_sheet.invoice_line.invoice_line_item_id
                product_in_warehouse.quantity=quantity
                product_in_warehouse.unit_name=warehouse_sheet.invoice_line.unit_name
                product_in_warehouse.warehouse_id=warehouse_sheet.warehouse_id
                product_in_warehouse.save()
            else:
                quantity=warehouse_sheet.invoice_line.quantity
                if warehouse_sheet.direction==WareHouseSheetDirectionEnum.OUT:
                    quantity=0-quantity
                product_in_warehouse.quantity=product_in_warehouse.quantity+quantity
                product_in_warehouse.save()
        message='با موفقیت نرمال سازی شد.'
        return SUCCEED,message,product_in_warehouse
    
    class Meta:
        verbose_name = _("ProductInWareHouse")
        verbose_name_plural = _("ProductInWareHouses")

    def __str__(self):
        return f"{self.warehouse} : {self.product} @ {self.quantity}  {self.unit_name}"