from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from django.views import View
from .forms import *
from .serializers import OrganizationalUnitSerializer,EmployeeSerializer
from .repo import OrganizationalUnitRepo,EmployeeRepo
from .apps import APP_NAME
from core.views import CoreContext,PageContext,MessageView
from utility.calendar import PersianCalendar
import json
from utility.enums import UnitNameEnum
from utility.log import leolog
from accounting.views import ProductContext,PageContext
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='organization/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context


def OrganizationalUnitContext(request,organizational_unit,*args, **kwargs):
    context=PageContext(request=request,page=organizational_unit)
    context['organizational_unit']=organizational_unit

    return context
  
 
def organizational_unit_employees_link(organizational_unit):
    result=''
    for employee in organizational_unit.employee_set.all():
        result+=f"""
        <a title="{employee.person_account.person.full_name}" href="{employee.get_absolute_url()}">
        <div class='text-center'>
        <img class="rounded-circle" width="64" src="{employee.person_account.person.image()}">
        </div>
        <div class='text-center'>
              <small class="text-muted mr-1">{employee.job_title}</small>
        </div>
        </a>
        """
    return result


def AddEmployeeContext(request,*args, **kwargs):
    context={}
    if request.user.has_perm(APP_NAME+".add_employee"):
        context['add_employee_form']=AddEmployeeForm()
        if 'organizational_unit' in kwargs:
            organizational_unit=kwargs['organizational_unit']
            organizational_units=[organizational_unit]
        else:
            organizational_units=OrganizationalUnitRepo(request=request).list()
        context['organizational_units_for_add_employee_form']=organizational_units
    return context
  

def SearchContext(request,search_for,*args, **kwargs):
    context={}
    WAS_FOUND=False
    

    organizational_units=OrganizationalUnitRepo(request=request).list(search_for=search_for)
    if len(organizational_units)>0:
        context['organizational_units']=organizational_units
        context['organizational_units_s']=json.dumps(OrganizationalUnitSerializer(organizational_units,many=True).data)
        WAS_FOUND=True


    employees=EmployeeRepo(request=request).list(search_for=search_for)
    if len(employees)>0:
        context['employees']=employees
        context['employees_s']=json.dumps(EmployeeSerializer(employees,many=True).data)
        WAS_FOUND=True


    context['WAS_FOUND']=WAS_FOUND
    return context


class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps

        return render(request,TEMPLATE_ROOT+"index.html",context)

  
class OrganizationalUnitView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        organizational_unit=OrganizationalUnitRepo(request=request).organizational_unit(*args, **kwargs)
        context.update(OrganizationalUnitContext(request=request,organizational_unit=organizational_unit))

        employees = organizational_unit.employee_set.all()
        context['employees']=employees
        employees_s=json.dumps(EmployeeSerializer(employees,many=True).data)
        context['employees_s']=employees_s

        
        # from projectmanager.views import ProjectRepo,ProjectSerializer
        # projects = ProjectRepo(request=request).list(organizational_unit_id=organizational_unit.id)
        # context['projects']=projects
        # projects_s=json.dumps(ProjectSerializer(projects,many=True).data)
        # context['projects_s']=projects_s




        
        organizational_units = OrganizationalUnitRepo(request=request).list(parent_id=organizational_unit.id)
        context['organizational_units']=organizational_units
        organizational_units_s=json.dumps(OrganizationalUnitSerializer(organizational_units,many=True).data)
        context['organizational_units_s']=organizational_units_s
        if request.user.has_perm(APP_NAME+'.add_organizationalunit'):
            context['add_organizational_unit_form']=AddOrganizationalUnitForm()


  
  
        if request.user.has_perm(APP_NAME+".add_employee"):
            context.update(AddEmployeeContext(request=request,organizational_unit=organizational_unit))

        return render(request,TEMPLATE_ROOT+"organizational-unit.html",context)


class OrganizationalUnitsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        organizational_units = OrganizationalUnitRepo(request=request).list(parent_id=None)

        context['organizational_units']=organizational_units
        organizational_units_s=json.dumps(OrganizationalUnitSerializer(organizational_units,many=True).data)
        context['organizational_units_s']=organizational_units_s
        if request.user.has_perm(APP_NAME+".add_organizational_unit"):
            context['add_organizational_unit_form']=AddOrganizationalUnitForm
        return render(request,TEMPLATE_ROOT+"organizational-units.html",context)


class EmployeeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        employee=EmployeeRepo(request=request).employee(*args, **kwargs)
        if employee is None:
            cc={
                'title':'',
                'body':'',
            }
            mv=MessageView(**cc)
            return mv.get(request=request)
        context['employee']=employee
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])
        return render(request,TEMPLATE_ROOT+"employee.html",context)


class EmployeesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        employees = EmployeeRepo(request=request).list(*args, **kwargs)

        context['employees']=employees
        employees_s=json.dumps(EmployeeSerializer(employees,many=True).data)
        context['employees_s']=employees_s
        if request.user.has_perm(APP_NAME+".add_employee"):
            context.update(AddEmployeeContext(request=request))
             
        return render(request,TEMPLATE_ROOT+"employees.html",context)

  
class TreeChartView(View):
    
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        organizational_unit=OrganizationalUnitRepo(request=request).organizational_unit(*args, **kwargs)
        if organizational_unit is None:
            title='واحد سازمانی وجود ندارد'
            body='واحد سازمانی وجود ندارد'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        
        context['organizational_unit']=organizational_unit  


        organizational_units=organizational_unit.all_sub_organizational_units()
        context['organizational_units']=organizational_units
        organizational_units_s=json.dumps(OrganizationalUnitSerializer(organizational_units,many=True).data)
        context['organizational_units_s']=organizational_units_s

        
        context['WIDE_LAYOUT']=True 
         
        
        pages=[{
                'title': f"""{organizational_unit.title}""",
                'parent_id': organizational_unit.parent_id,
                'parent': 0,
                'get_absolute_url': organizational_unit.get_absolute_url(),
                'id': organizational_unit.id,
                'pre_title': "",
                'color': organizational_unit.color,
                'sub_title':organizational_unit_employees_link(organizational_unit),
                }]
          
        for organizational_unit in organizational_units:
            pages.append({
                'title': f"""{organizational_unit.title}""",
                'parent_id': organizational_unit.parent_id,
                'parent': 0,
                'get_absolute_url': organizational_unit.get_absolute_url(),
                'id': organizational_unit.id,
                'pre_title': "",
                'color': organizational_unit.color,
                'sub_title':organizational_unit_employees_link(organizational_unit),
                })

        context['pages_s'] = json.dumps(pages)
        return render(request,TEMPLATE_ROOT+"tree-chart.html",context) 
