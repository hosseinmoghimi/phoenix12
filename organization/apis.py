
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import OrganizationalUnitRepo,EmployeeRepo
from .serializers import OrganizationalUnitSerializer,EmployeeSerializer
from django.http import JsonResponse
from .forms import *
   
 
class AddEmployeeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_employee_form=AddEmployeeForm(request.POST)
        if add_employee_form.is_valid():
            log=333
            cd=add_employee_form.cleaned_data
            result,message,employee=EmployeeRepo(request=request).add_employee(**cd)
            if employee is not None:
                context['employee']=EmployeeSerializer(employee).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class AddOrganizationalUnitApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_organizational_unit_form=AddOrganizationalUnitForm(request.POST)
        if add_organizational_unit_form.is_valid():
            log=333
            cd=add_organizational_unit_form.cleaned_data
            result,message,organizational_unit=OrganizationalUnitRepo(request=request).add_organizational_unit(**cd)
            if result==SUCCEED:
                context['organizational_unit']=OrganizationalUnitSerializer(organizational_unit).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class SelectOrganizationalUnitApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_organizational_unit_form=SelectOrganizationalUnitForm(request.POST)
            if select_organizational_unit_form.is_valid():
                log=333
                cd=select_organizational_unit_form.cleaned_data
                organizational_unit=OrganizationalUnitRepo(request=request).organizational_unit(**cd)
                if organizational_unit is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['organizational_unit']=OrganizationalUnitSerializer(organizational_unit).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

 
class SelectEmployeeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            select_employee_form=SelectEmployeeForm(request.POST)
            if select_employee_form.is_valid():
                log=333
                cd=select_employee_form.cleaned_data
                employee=EmployeeRepo(request=request).employee(**cd)
                if employee is not None:
                    result=SUCCEED
                    message="موفقیت آمیز"
                    context['employee']=EmployeeSerializer(employee).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


 