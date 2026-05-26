from organization.repo import EmployeeRepo,OrganizationalUnitRepo
from .models import ProductInWareHouse,WareHouse,WareHouseSheet,WareHouseSheetSignature,WareHouseSheetLabel
from .apps import APP_NAME
from .enums import *
from utility.enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *
from accounting.repo import InvoiceLine,FinancialEventStatusEnum,InvoiceRepo



class WareHouseRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=WareHouse.objects.filter(id=0)
        person=PersonRepo(request=request).me
        me_employee=EmployeeRepo(request=request).me
        if person is not None:
            if request.user.has_perm(APP_NAME+".view_warehouse"):
                self.objects=WareHouse.objects.all()
            elif me_employee is not None:
                self.objects=me_employee.warehouse_set.all()


    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(person_account__person__full_name__contains=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def warehouse(self,*args, **kwargs):
        if "warehouse_id" in kwargs and kwargs["warehouse_id"] is not None:
            return self.objects.filter(pk=kwargs['warehouse_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_warehouse(self,*args,**kwargs):
        result,message,warehouse=FAILED,"",None
        
        if len(WareHouse.objects.filter(name=kwargs["name"]))>0:
            message='نام تکراری برای انبار جدید'
            return FAILED,message,None 
        if not self.request.user.has_perm(APP_NAME+".add_warehouse"):
            message="دسترسی غیر مجاز"
            return result,message,warehouse

        warehouse=WareHouse()
        if 'name' in kwargs:
            warehouse.name=kwargs["name"]  
        if 'person_account_id' in kwargs:
            warehouse.person_account_id=kwargs["person_account_id"]
          
        (result,message,warehouse)=warehouse.save()
        return result,message,warehouse


class WareHouseSheetLabelRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=WareHouseSheetLabel.objects.filter(id=0)
        self.me_person=PersonRepo(request=request).me
        if self.me_person is not None:
            if request.user.has_perm(APP_NAME+".view_account"):
                self.objects=WareHouseSheetLabel.objects
                self.my_accounts=self.objects 
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "warehouse_id" in kwargs:
            warehouse_id=kwargs["warehouse_id"]
            objects=objects.filter(warehouse_id=warehouse_id) 
        if "warehouse_sheet_id" in kwargs:
            warehouse_sheet_id=kwargs["warehouse_sheet_id"]
            objects=objects.filter(warehouse_sheet_id=warehouse_sheet_id)  
        if "invoice_line_item_id" in kwargs:
            invoice_line_item_id=kwargs["invoice_line_item_id"]
            objects=objects.filter(invoice_line__invoice_line_item_id=invoice_line_item_id) 
        if "product_id" in kwargs:
            product_id=kwargs["product_id"]
            objects=objects.filter(invoice_line__invoice_line_item_id=product_id) 
        if "invoice_line_id" in kwargs:
            invoice_line_id=kwargs["invoice_line_id"]
            objects=objects.filter(invoice_line_id=invoice_line_id) 
        if "invoice_id" in kwargs:
            invoice_id=kwargs["invoice_id"]
            objects=objects.filter(invoice_line__invoice_id=invoice_id) 
        return objects.all()
        
    def warehouse_sheet_label(self,*args, **kwargs):
        if "warehouse_id" in kwargs and kwargs["warehouse_id"] is not None:
            return self.objects.filter(pk=kwargs['warehouse_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_warehouse_sheet_label(self,*args,**kwargs):
        result,message,warehouse_sheet_label=FAILED,"",None
        
        
        if not self.request.user.has_perm(APP_NAME+".add_warehousesheetlabel"):
            message="دسترسی غیر مجاز"
            return result,message,warehouse_sheet_label

        warehouse_sheet_label=WareHouseSheetLabel()
        warehouse_sheet=WareHouseSheet.objects.filter(pk=kwargs["warehouse_sheet_id"]).first()
        if warehouse_sheet is None:
            message='برگه انبار درست انتخاب نشده است.'
            return result,message,None    
        me_employee=EmployeeRepo(request=self.request).me
        if me_employee is None:
            return FAILED,'شما حق امضا ندارید.',None
        warehouse_sheet_label.employee_id=me_employee.id

            
        if 'warehouse_sheet_id' in kwargs:
            warehouse_sheet_label.warehouse_sheet_id=kwargs["warehouse_sheet_id"]  

        if 'description' in kwargs:
            warehouse_sheet_label.description=kwargs["description"]  


        if 'serial_no' in kwargs:
            warehouse_sheet_label.serial_no=kwargs["serial_no"]  

 
        warehouse_sheet_label.save()
        if warehouse_sheet_label.id is not None:
            result=SUCCEED
            message='امضای برگه انبار با موفقیت ذخیره شد.'
        return result,message,warehouse_sheet_label
 

class WareHouseSheetRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.me_person=PersonRepo(request=request).me
        self.me_employee=EmployeeRepo(request=request).me
        self.objects=WareHouseSheet.objects.filter(pk=0)
        if self.me_employee is not None:
            self.objects=WareHouseSheet.objects.filter(employee_id=self.me_employee.id)
        if self.me_person is not None:
            if request.user.has_perm(APP_NAME+".view_warehousesheet"):
                self.objects=WareHouseSheet.objects
                
            elif self.me_employee is not None :
                for warehouse in self.me_employee.warehouse_set.all():
                    self.objects=WareHouseSheet.objects.filter(warehouse_id=warehouse.id).filter(status=SignatureStatusEnum.CONFIRMED)

    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "warehouse_id" in kwargs:
            warehouse_id=kwargs["warehouse_id"]
            objects=objects.filter(warehouse_id=warehouse_id)  
        if "invoice_line_item_id" in kwargs:
            invoice_line_item_id=kwargs["invoice_line_item_id"]
            objects=objects.filter(invoice_line__invoice_line_item_id=invoice_line_item_id) 
        if "product_id" in kwargs:
            product_id=kwargs["product_id"]
            objects=objects.filter(invoice_line__invoice_line_item_id=product_id) 
        if "invoice_line_id" in kwargs:
            invoice_line_id=kwargs["invoice_line_id"]
            objects=objects.filter(invoice_line_id=invoice_line_id) 
        if "invoice_id" in kwargs:
            invoice_id=kwargs["invoice_id"]
            objects=objects.filter(invoice_line__invoice_id=invoice_id) 
        return objects.all()
        
    def warehouse_sheet(self,*args, **kwargs):
        if "warehouse_id" in kwargs and kwargs["warehouse_id"] is not None:
            return self.objects.filter(pk=kwargs['warehouse_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
    def add_material_request(self,*args, **kwargs):
        result,message,warehouse_sheet,invoice_line=FAILED,"",None,None
        

        me_employee=EmployeeRepo(request=self.request).me
        sw=False
        message="دسترسی غیر مجاز"
        if self.request.user.has_perm(APP_NAME+".add_warehousesheet"):
            sw=True
        if not sw and me_employee is not None:
            sw=True

        if not sw:
            return FAILED,message,None,None

        invoice_line=InvoiceLine(person_id=self.me_person.id)
        invoice_line_item_id=0
        if 'invoice_line_item_id' in kwargs:
            invoice_line_item_id=kwargs["invoice_line_item_id"]
            invoice_line.invoice_line_item_id=invoice_line_item_id

        if 'product_id' in kwargs:
            invoice_line_item_id=kwargs["product_id"]
            invoice_line.invoice_line_item_id=invoice_line_item_id

        if 'invoice_id' in kwargs:
            if kwargs['invoice_id']>0:
                invoice_line.invoice_id=kwargs["invoice_id"]
                invoice=InvoiceRepo(request=self.request).invoice(id=kwargs["invoice_id"])
                if invoice is None:
                    message='فاکتور مورد نظر وجود ندارد.'
                    return FAILED,message,None,None
                
                if invoice.status==FinancialEventStatusEnum.APPROVED:
                    message='فاکتور تایید شده و امکان تغییر ، ویرایش و افزودن سطر وجود ندارد.'
                    return FAILED,message,None,None
                
                if invoice.status==FinancialEventStatusEnum.DELIVERED:
                    message='فاکتور تحویل شده و امکان تغییر ، ویرایش و افزودن سطر وجود ندارد.'
                    return FAILED,message,None,None
                
                if invoice.status==FinancialEventStatusEnum.FINISHED:
                    message='فاکتور نهایی شده و امکان تغییر ، ویرایش و افزودن سطر وجود ندارد.'
                    return FAILED,message,None,None
        
        if 'description' in kwargs:
            invoice_line.description=kwargs["description"]
        if 'status' in kwargs:
            invoice_line.status=kwargs["status"]
        if 'quantity' in kwargs:
            invoice_line.quantity=kwargs["quantity"]
        if 'unit_price' in kwargs:
            unit_price=kwargs["unit_price"]
            invoice_line.unit_price=unit_price

        if 'unit_name' in kwargs:
            unit_name=kwargs["unit_name"]
            invoice_line.unit_name=unit_name

        if 'save' in kwargs or kwargs["default_price"]:
            save=kwargs["save"]
            if save or kwargs["default_price"]:
                if 'coef' in kwargs:
                    coef=kwargs["coef"]
                if 'default_price' in kwargs:
                    default_price=kwargs["default_price"]
                try:
                    InvoiceLineItemUnitRepo(request=self.request).add_invoice_line_item_unit(
                        invoice_line_item_id=invoice_line_item_id,
                        coef=coef,
                        default=default_price,
                        unit_name=unit_name,
                        unit_price=unit_price,)
                except:
                    pass
        result,message,invoice_line=invoice_line.save()
        # self.add_warehouse_sheet()
        warehouse_sheet=WareHouseSheet()
        warehouse_sheet.invoice_line_id=invoice_line.id
        

        
         
        if 'warehouse_id' in kwargs:
            warehouse=WareHouseRepo(request=self.request).warehouse(pk=kwargs["warehouse_id"])
            if warehouse is not None:
                warehouse_sheet.warehouse_id=warehouse.id
 
 
        if 'invoice_id' in kwargs:
            invoice=InvoiceRepo(request=self.request).invoice(pk=kwargs["invoice_id"])
            if invoice is not None:
                warehouse_sheet.invoice_id=invoice.id


        if 'col' in kwargs:
            warehouse_sheet.col=kwargs["col"]  


            
        if 'row' in kwargs:
            warehouse_sheet.row=kwargs["row"]  

            
        if 'shelf' in kwargs:
            warehouse_sheet.shelf=kwargs["shelf"]  




        if 'status' in kwargs and kwargs['status'] is not None and len(kwargs['status'])>0:
            warehouse_sheet.status=kwargs["status"]  



        if 'type' in kwargs and kwargs['type'] is not None and len(kwargs['type'])>0:
            warehouse_sheet.type=kwargs["type"]  



        if 'description' in kwargs:
            warehouse_sheet.description=kwargs["description"]  


        if 'direction' in kwargs:
            warehouse_sheet.direction=kwargs["direction"]  
        
        if 'organizational_unit_id' in kwargs:
            
            organizational_unit=OrganizationalUnitRepo(request=self.request).organizational_unit(pk=kwargs["organizational_unit_id"])
            if organizational_unit is not None:
                warehouse_sheet.organizational_unit_id=organizational_unit.id
 
                 

        warehouse_sheet.employee=self.me_employee
        warehouse_sheet.save()
        ProductInWareHouseRepo(request=self.request).normalize_product_in_warehouse(warehouse_id=warehouse_sheet.warehouse.id,product_id=warehouse_sheet.invoice_line.invoice_line_item.id)


        warehouse_sheet_signature=WareHouseSheetSignature()
        warehouse_sheet_signature.warehouse_sheet=warehouse_sheet
        warehouse_sheet_signature.employee=self.me_employee
        warehouse_sheet_signature.status=SignatureStatusEnum.REQUESTED
        warehouse_sheet_signature.save()

        return result,message,warehouse_sheet,invoice_line


    def add_warehouse_sheet(self,*args,**kwargs):
        result,message,warehouse_sheet=FAILED,"",None
        
        
        if not self.request.user.has_perm(APP_NAME+".add_warehousesheet"):
            message="دسترسی غیر مجاز"
            return result,message,warehouse_sheet

        warehouse_sheet=WareHouseSheet()
        warehouse=WareHouse.objects.filter(pk=kwargs["warehouse_id"]).first()
        if warehouse is None:
            message='انبار درست انتخاب نشده است.'
            return result,message,None    
         
        if 'warehouse_id' in kwargs:
            warehouse_sheet.warehouse_id=kwargs["warehouse_id"]  

        if 'organizational_unit_id' in kwargs:
            warehouse_sheet.organizational_unit_id=kwargs["organizational_unit_id"]
          
        if 'invoice_line_id' in kwargs:
            warehouse_sheet.invoice_line_id=kwargs["invoice_line_id"]
          
        if 'col' in kwargs:
            warehouse_sheet.col=kwargs["col"]  

        if 'status' in kwargs and kwargs['status'] is not None and len(kwargs['status'])>0:
            warehouse_sheet.status=kwargs["status"]  

        if 'type' in kwargs and kwargs['type'] is not None and len(kwargs['type'])>0:
            warehouse_sheet.type=kwargs["type"]  
            
        if 'row' in kwargs:
            warehouse_sheet.row=kwargs["row"]  
            
        if 'shelf' in kwargs:
            warehouse_sheet.shelf=kwargs["shelf"]  

        if 'description' in kwargs:
            warehouse_sheet.description=kwargs["description"]  

        if 'direction' in kwargs:
            warehouse_sheet.direction=kwargs["direction"]  

        if self.me_employee is None:
            message="کاربر شما پرسنل مجاز برای افزودن درخواست ندارد."
            return FAILED,message,None
        warehouse_sheet.employee=self.me_employee
        warehouse_sheet.save()
        if warehouse_sheet.id is not None:
            result=SUCCEED
            message='برگه انبار با موفقیت ذخیره و امضا شد.'

        warehouse_sheet_signature=WareHouseSheetSignature()
        warehouse_sheet_signature.warehouse_sheet=warehouse_sheet
        warehouse_sheet_signature.employee=self.me_employee
        warehouse_sheet_signature.status=SignatureStatusEnum.REQUESTED
        warehouse_sheet_signature.save()
        

        return result,message,warehouse_sheet

    def add_invoice_warehouse_sheets(self,*args, **kwargs):
        message=''
        invoice_id=kwargs['invoice_id']
        from accounting.repo import InvoiceRepo
        invoice=InvoiceRepo(request=self.request).invoice(invoice_id=invoice_id)
        if invoice is None:
            message='فاکتور پیدا نشد.'
            return FAILED,message,[]
        warehouse_sheets=[]
        for invoice_line in invoice.invoiceline_set.all():
            invoice_line_id=invoice_line.id
            kwargs['invoice_line_id']=invoice_line_id
            result,message,warehouse_sheet=self.add_warehouse_sheet(**kwargs)
            if result==SUCCEED:
                warehouse_sheets.append(warehouse_sheet)
        return SUCCEED,message,warehouse_sheets
        

class ProductInWareHouseRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=ProductInWareHouse.objects.filter(id=0)
        person=PersonRepo(request=request).me
        me_employee=EmployeeRepo(request=request).me
        if person is not None:
            if request.user.has_perm(APP_NAME+".view_productinwarehouse"):
                self.objects=ProductInWareHouse.objects.all()
             
    def normalize_product_in_warehouse(self,*args, **kwargs):
        result,message,product_in_warehouse=FAILED,"",None
        # if not self.request.user.has_perm(APP_NAME+".delete_productinwarehouse"):
        #     message='دسترسی شما برای این فرآیند مجاز نمی باشد.'
        #     return FAILED,message,None
        ProductInWareHouse.normalize_products_in_warehouse(**kwargs)
        message='با موفقیت نرمال سازی شد.'
        return SUCCEED,message,None
    def list(self,*args, **kwargs):
        # if self.request.user 
        objects=self.objects
        if "product_id" in kwargs:
            product_id=kwargs["product_id"]
            if product_id is not None:
                objects=objects.filter(product_id=product_id)  

        if "warehouse_id" in kwargs:
            warehouse_id=kwargs["warehouse_id"]
            if warehouse_id is not None:
                objects=objects.filter(warehouse_id=warehouse_id)  

        return objects.all()
        
    def product_in_warehouse(self,*args, **kwargs):
        if "product_in_warehouse_id" in kwargs and kwargs["product_in_warehouse_id"] is not None:
            return self.objects.filter(pk=kwargs['product_in_warehouse_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_product_in_warehouse(self,*args,**kwargs):
        result,message,product_in_warehouse=FAILED,"",None
        
        if len(ProductInWareHouse.objects.filter(name=kwargs["name"]))>0:
            message='نام تکراری برای انبار جدید'
            return FAILED,message,None 
        if not self.request.user.has_perm(APP_NAME+".add_productinwarehouse"):
            message="دسترسی غیر مجاز"
            return result,message,product_in_warehouse

        product_in_warehouse=ProductInWareHouse()
        if 'name' in kwargs:
            product_in_warehouse.name=kwargs["name"]  
        if 'person_account_id' in kwargs:
            product_in_warehouse.person_account_id=kwargs["person_account_id"]
          
        (result,message,product_in_warehouse)=product_in_warehouse.save()
        return result,message,product_in_warehouse


class WareHouseSheetSignatureRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=WareHouseSheetSignature.objects.filter(id=0)
        self.me_person=PersonRepo(request=request).me
        if self.me_person is not None:
            if request.user.has_perm(APP_NAME+".view_warehousesheetsignature"):
                self.objects=WareHouseSheetSignature.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "warehouse_id" in kwargs:
            warehouse_id=kwargs["warehouse_id"]
            objects=objects.filter(warehouse_id=warehouse_id) 
        if "warehouse_sheet_id" in kwargs:
            warehouse_sheet_id=kwargs["warehouse_sheet_id"]
            objects=objects.filter(warehouse_sheet_id=warehouse_sheet_id)  
        if "invoice_line_item_id" in kwargs:
            invoice_line_item_id=kwargs["invoice_line_item_id"]
            objects=objects.filter(invoice_line__invoice_line_item_id=invoice_line_item_id) 
        if "product_id" in kwargs:
            product_id=kwargs["product_id"]
            objects=objects.filter(invoice_line__invoice_line_item_id=product_id) 
        if "invoice_line_id" in kwargs:
            invoice_line_id=kwargs["invoice_line_id"]
            objects=objects.filter(invoice_line_id=invoice_line_id) 
        if "invoice_id" in kwargs:
            invoice_id=kwargs["invoice_id"]
            objects=objects.filter(invoice_line__invoice_id=invoice_id) 
        return objects.all()
        
    def warehouse_sheet_signature(self,*args, **kwargs):
        if "warehouse_id" in kwargs and kwargs["warehouse_id"] is not None:
            return self.objects.filter(pk=kwargs['warehouse_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_warehouse_sheet_signature(self,*args,**kwargs):
        result,message,warehouse_sheet_signature=FAILED,"",None
        
        
        if not self.request.user.has_perm(APP_NAME+".add_warehousesheetsignature"):
            message="دسترسی غیر مجاز"
            return result,message,warehouse_sheet_signature

        warehouse_sheet_signature=WareHouseSheetSignature()
        warehouse_sheet=WareHouseSheet.objects.filter(pk=kwargs["warehouse_sheet_id"]).first()
        if warehouse_sheet is None:
            message='برگه انبار درست انتخاب نشده است.'
            return result,message,None    
        me_employee=EmployeeRepo(request=self.request).me
        if me_employee is None:
            return FAILED,'شما حق امضا ندارید.',None
        warehouse_sheet_signature.employee_id=me_employee.id

            
        if 'warehouse_sheet_id' in kwargs:
            warehouse_sheet_signature.warehouse_sheet_id=kwargs["warehouse_sheet_id"]  

        if 'description' in kwargs:
            warehouse_sheet_signature.description=kwargs["description"]  


        if 'status' in kwargs:
            warehouse_sheet_signature.status=kwargs["status"]  

 
        warehouse_sheet_signature.save()
        if warehouse_sheet_signature.id is not None:
            result=SUCCEED
            message='امضای برگه انبار با موفقیت ذخیره شد.'
        return result,message,warehouse_sheet_signature
 