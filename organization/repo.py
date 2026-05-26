from .models import OrganizationalUnit,Employee 
from .apps import APP_NAME
from .enums import *
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
 

class OrganizationalUnitRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=OrganizationalUnit.objects.filter(id=0)
        person=PersonRepo(request=request).me
        if person is not None:
            if request.user.has_perm(APP_NAME+".view_organizationalunit"):
                self.objects=OrganizationalUnit.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(person_account__person__full_name__contains=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def organizational_unit(self,*args, **kwargs):
        if "organizational_unit_id" in kwargs and kwargs["organizational_unit_id"] is not None:
            return self.objects.filter(pk=kwargs['organizational_unit_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_organizational_unit(self,*args,**kwargs):
        result,message,organizational_unit=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_organizationalunit"):
            message="دسترسی غیر مجاز"
            return result,message,organizational_unit
        if len(OrganizationalUnit.objects.filter(title=kwargs['title']))>0:
            message="عنوان تکراری"
            return result,message,organizational_unit
         
        organizational_unit=OrganizationalUnit()
        if 'name' in kwargs:
            organizational_unit.name=kwargs["name"]
        if 'parent_id' in kwargs :
            if kwargs["parent_id"] is not None and kwargs["parent_id"]>0:
                organizational_unit.parent_id=kwargs["parent_id"]

        if 'person_account_id' in kwargs:
            organizational_unit.person_account_id=kwargs["person_account_id"]
            # from accounting.models import Account
            # account=Account.objects.filter(id=kwargs['account_id']).first()
            # if account is not None:
            #     organizational_unit.account_code=account.code
          

        if 'title' in kwargs:
            organizational_unit.title=kwargs["title"]
        
        (result,message,organizational_unit)=organizational_unit.save()
        return result,message,organizational_unit
 

class EmployeeRepo():
    def __init__(self,request,*args, **kwargs):
        self.my_accounts=[]
        self.request=request
        self.objects=Employee.objects.filter(id=0)
        me_person=PersonRepo(request=request).me
        self.me=None
        if me_person is not None:
            self.me=Employee.objects.filter(person_account__person_id=me_person.id).first()
        if request.user.has_perm(APP_NAME+".view_employee"):
            self.objects=Employee.objects
            
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(job_title=search_for) | Q(person_account__person__full_name__contains=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def employee(self,*args, **kwargs):
        if "employee_id" in kwargs and kwargs["employee_id"] is not None:
            return self.objects.filter(pk=kwargs['employee_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_employee(self,*args,**kwargs):
        result,message,employee=FAILED,"",None
        if len(Employee.objects.filter(job_title=kwargs['job_title']).filter(person_account_id=kwargs['person_account_id']).filter(organizational_unit_id=kwargs['organizational_unit_id']))>0:
            message="پرسنل تکراری"
            return result,message,None
        

        if not self.request.user.has_perm(APP_NAME+".add_organizationalunit"):
            message="دسترسی غیر مجاز"
            return result,message,employee
        employee=Employee()
        if 'job_title' in kwargs:
            employee.job_title=kwargs["job_title"]
        if 'person_account_id' in kwargs:
            if kwargs["person_account_id"]>0:
                employee.person_account_id=kwargs["person_account_id"]
        if 'organizational_unit_id' in kwargs:
            if kwargs["organizational_unit_id"]>0:
                employee.organizational_unit_id=kwargs["organizational_unit_id"]
         


        if 'title' in kwargs:
            employee.title=kwargs["title"]
        
        (result,message,employee)=employee.save()
        return result,message,employee

 