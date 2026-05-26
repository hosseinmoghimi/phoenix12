from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  

    path('organizational-unit/add/',login_required(apis.AddOrganizationalUnitApi.as_view()),name="add_organizational_unit"),  
    path('organizational-units/',login_required(views.OrganizationalUnitsView.as_view()),name="organizational_units"),  
    path('organizational-unit/<int:pk>/',login_required(views.OrganizationalUnitView.as_view()),name="organizationalunit"), 
    path('tree-chart/<int:pk>/',login_required(views.TreeChartView.as_view()),name="tree_chart"), 

    path('select-organizational-unit/',login_required(apis.SelectOrganizationalUnitApi.as_view()),name="select_organizational_unit"),  
    path('select-employee/',login_required(apis.SelectEmployeeApi.as_view()),name="select_employee"),  

     
    path('employee/add/',login_required(apis.AddEmployeeApi.as_view()),name="add_employee"),  
    path('employees/',login_required(views.EmployeesView.as_view()),name="employees"),  
    path('employee/<int:pk>/',login_required(views.EmployeeView.as_view()),name="employee"), 
   
]
