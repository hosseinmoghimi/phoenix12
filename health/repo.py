from .models import Drug
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from utility.calendar import PersianCalendar,to_gregorian
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .constants import EXCEL_DRUGS_DATA_START_ROW
from core.repo import Repo
 

class DrugRepo(Repo):
    def __init__(self,request,*args, **kwargs):
        super(DrugRepo,self).__init__(request=request,app_name=APP_NAME,*args, **kwargs)
        self.request=request
        self.objects=Drug.objects.filter(id=0)
        if request.user.has_perm(APP_NAME+".view_drug"):
            self.objects=Drug.objects 
         
       
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "supplier_id" in kwargs:
            supplier_id=kwargs["supplier_id"]
            objects=objects.filter(supplier_id=supplier_id)
        if "product_id" in kwargs:
            product_id=kwargs["product_id"]
            objects=objects.filter(product_id=product_id)
        if "region_id" in kwargs:
            region_id=kwargs["region_id"]
            objects=objects.filter(region_id=region_id)
        if "group_id" in kwargs:
            group_id=kwargs["group_id"]
            objects=objects.filter(group_id=group_id)
          
        return objects.all()
        
    def drug(self,*args, **kwargs):
        if "drug_id" in kwargs and kwargs["drug_id"] is not None:
            return self.objects.filter(pk=kwargs['drug_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
    def add_drug(self,*args,**kwargs):
        result,message,drug=FAILED,"",None
        
        me_supplier=SupplierRepo(request=self.request).me

        if me_supplier is None:
            if self.request.user.has_perm(APP_NAME+".add_drug"):
                if 'supplier_id' in kwargs:
                    supplier_id=kwargs["supplier_id"]
            else:
                message="دسترسی غیر مجاز"
                return result,message,drug
        else:
            supplier_id=me_supplier.id
        drug=Drug(supplier_id=supplier_id)
         
        if 'unit_price' in kwargs:
            if kwargs["unit_price"]>0:
                drug.unit_price=kwargs["unit_price"]
        if 'coef' in kwargs:
            drug.coef=kwargs["coef"]
            
        if 'unit_name' in kwargs:
            drug.unit_name=kwargs["unit_name"]
         
        if 'available' in kwargs:
            drug.available=kwargs["available"]
            drug.quantity=kwargs["available"]
         
        if 'region_id' in kwargs:
            drug.region_id=kwargs["region_id"]
        if 'group_id' in kwargs:
            drug.group_id=kwargs["group_id"]
        if 'product_id' in kwargs:
            drug.product_id=kwargs["product_id"]
        if 'start_date' in kwargs:
            start_date=kwargs["start_date"]
            drug.start_date=to_gregorian(start_date)
        if 'end_date' in kwargs:
            end_date=kwargs["end_date"]
            drug.end_date=to_gregorian(end_date)



        if 'discount_percentage' in kwargs:
            drug.discount_percentage=kwargs["discount_percentage"]
        
        
         
        (result,message,drug)=drug.save()
        return result,message,drug

    def import_drugs_from_excel(self,*args,**kwargs):
        result,message,drugs=FAILED,"",[]
        excel_file=kwargs['excel_file']
        # import pandas
        
        # df = pandas.read_excel(excel_file)
        # drugs=[]
        # for row in df.columns[0]:
        #     print (df.columns)
        import openpyxl 

        wb = openpyxl.load_workbook(excel_file)
        try:
            ws = wb['drugs']
        
        except:
            message='فایل شما برگه آماده فروش ها ندارد.'
            return result,message,None
        count=kwargs['count']
        try:
            count=int(ws.cell(row=1, column=2).value)
        except:
            
            message='فایل برگه حساب ها ، تعداد ندارد.'
            return result,message,None  
        drugs_to_import=[]
        START_ROW=EXCEL_SHOPS_DATA_START_ROW
        for i in range(START_ROW,count+START_ROW):
            drug={}
            
            
            i=str(i) 
            # product['id']=ws['A'+str(i)].value
            iiiddd=ws['A'+i].value
            if iiiddd is not None:
                id=int(ws['B'+i].value) 
                product_id=int(ws['E'+i].value)
                product_barcode=(ws['F'+i].value)
                supplier_id=int(ws['C'+i].value)
                group_id=int(ws['H'+i].value)
                region_id=int(ws['J'+i].value)
                quantity=int(ws['L'+i].value)
                unit_price=int(ws['O'+i].value)
                unit_name=(ws['M'+i].value)
                start_date=(ws['P'+i].value)
                end_date=(ws['Q'+i].value)
                discount_percentage=(ws['N'+i].value)

                drug['id']=0
                drug['product_id']=product_id
                drug['product_barcode']=product_barcode
                drug['supplier_id']=supplier_id
                drug['quantity']=quantity
                drug['group_id']=group_id
                drug['region_id']=region_id
                drug['unit_price']=unit_price
                drug['unit_name']=unit_name
                drug['start_date']=start_date
                drug['end_date']=end_date
                drug['discount_percentage']=discount_percentage
                drugs_to_import.append(drug) 
        modified=added=0
        for drug in drugs_to_import:
            from accounting.repo import ProductRepo
            from utility.repo import RegionRepo
            product=ProductRepo(request=self.request).product(barcode=drug["product_barcode"],product_id=drug['product_id'])
            supplier=SupplierRepo(request=self.request).supplier(supplier_id=drug["supplier_id"])
            region=RegionRepo(request=self.request).region(region_id=drug["region_id"])
            group=CustomerGroupRepo(request=self.request).customer_group(customer_group_id=drug["group_id"])
            Drug.objects.filter(supplier_id=supplier.id).filter(product_id=product.id).filter(region_id=region.id).filter(group_id=group.id).delete()
            result,message,new_drug=self.add_drug(
                product_id=product.id,
                supplier_id=supplier.id,
                group_id=group.id,
                region_id=region.id,
                unit_price=drug['unit_price'],
                unit_name=drug['unit_name'],
                quantity=drug['quantity'],
                available=drug['quantity'],
                discount_percentage=drug['discount_percentage'],
                start_date=PersianCalendar().to_gregorian(drug['start_date']),
                end_date=PersianCalendar().to_gregorian(drug['end_date']),
                                                        
            )
            drugs.append(new_drug)
               
                # new_drug.title=drug["title"]
                # new_drug.barcode=drug["barcode"]
                # new_drug.unit_name=drug["unit_name"]
                # new_drug.unit_price=drug["unit_price"] 
                # new_drug.save()
            if result==SUCCEED:
                added+=1
        result=SUCCEED
        message=f"""{added} آماده فروش اضافه شد.
                    <br>
                    {modified} آماده فروش ویرایش شد. """
        drugs=self.list()


        if True:
            log_data={}
            from log.repo import LogRepo
            log_data['person_id']=PersonRepo(request=self.request).me.id
            log_data['url']=reverse("market:drugs")
            log_data['title']="بازیابی آماده فروش ها"
            log_data['description']=message
            log_data['app_name']=APP_NAME
            LogRepo(request=self.request).add_log(**log_data)
        
        return result,message,drugs
    
