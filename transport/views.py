from utility.views import MessageView
from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .serializers import VehicleStatusSerializer,WorkShiftSerializer,MaintenanceSerializer,VehicleSerializer,ServiceManSerializer,DriverSerializer
from .repo import VehicleRepo,VehicleStatusRepo,WorkShiftRepo,ServiceManRepo,MaintenanceRepo,DriverRepo,AnbarProductRepo,ServiceRepo
from .forms import *
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
import json
from django.views import View
from core.views import CoreContext,leolog,PageContext
from accounting.views import AssetContext,AddInvoiceContext,InvoiceSerializer,InvoiceLineWithInvoiceSerializer
from .enums import MaintenanceTypesEnum,OilTypeEnum
from .enums import FilterTypeEnum,FilterActionEnum,TavaghofCausesEnum
from .serializers import OilServiceSerializer,FilterServiceSerializer,ProductSerializer,TavaghofSerializer,ServiceSerializer,AnbarProductSerializer

from .serializers import VehicleEventSerializer
from .repo import VehicleEventRepo,TavaghofRepo
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='transport/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"

def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    context['title']="حمل و نقل"

    context[WIDE_LAYOUT]=False 
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
 
def AddMaintenanceContext(request):
    context={}
    context['add_maintenance_form']=AddMaintenanceForm()
    vehicles=VehicleRepo(request=request).list()
    service_mans=ServiceManRepo(request=request).list()
    context['vehicles']=vehicles
    context['service_mans']=service_mans
    drivers=DriverRepo(request=request).list()
    context['drivers']=drivers
    maintenance_types=(i[0] for i in MaintenanceTypesEnum.choices)
    context['maintenance_types']=maintenance_types
    return context
 
def AddOilingMaintenanceContext(request):
    context=AddMaintenanceContext(request=request)
    context['oil_types']=(i[0] for i in OilTypeEnum.choices)
    return context

def VehicleContext(request,vehicle,*args, **kwargs):
    context=AssetContext(request=request,asset=vehicle)
    if request.user.has_perm('accounting.add_maintenance'):
        context.update(AddMaintenanceContext(request=request))
    maintenances=MaintenanceRepo(request=request).list(vehicle_id=vehicle.id)
    maintenances_s=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
    context['maintenances']=maintenances
    context['maintenances_s']=maintenances_s





    service_mans=ServiceManRepo(request=request).list(vehicle_id=vehicle.id)
    service_mans_s=json.dumps(ServiceManSerializer(service_mans,many=True).data)
    context['service_mans']=service_mans
    context['service_mans_s']=service_mans_s

    return context 

def AddOilingMaintenanceDetailContext(request):
    context={}
    context['add_oiling_maintenance_detail_form']=AddOilingMaintenanceDetailForm()
    from .enums import FilterActionEnum,FilterTypeEnum
    context['filter_actions']=(i[0] for i in FilterActionEnum.choices)
    context['filter_types']=(i[0] for i in FilterTypeEnum.choices)
    return context
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)
 

class VehiclesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        vehicles =VehicleRepo(request=request).list(*args, **kwargs)
        context['vehicles']=vehicles
        vehicles_s=json.dumps(VehicleSerializer(vehicles,many=True).data)
        context['vehicles_s']=vehicles_s
 
        context[WIDE_LAYOUT]=False
        if request.user.has_perm(APP_NAME+'.add_vehicle'):
            context['add_vehicle_form']=AddVehicleForm()
            from .enums import VehicleTypeEnum,VehicleColorEnum,VehicleBrandEnum
            context['vehicle_types']=(i[0] for i in VehicleTypeEnum.choices)
            context['vehicle_colors']=(i[0] for i in VehicleColorEnum.choices)
            context['brand_names']=(i[0] for i in VehicleBrandEnum.choices)
            context['drivers']=DriverRepo(request=request).list()
        return render(request,TEMPLATE_ROOT+"vehicles.html",context) 
    
    
class ReportView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['title']="گزارشگیری دستگاه ها"
        vehicles =VehicleRepo(request=request).list(*args, **kwargs)
        context['vehicles']=vehicles
        vehicles_s=json.dumps(VehicleSerializer(vehicles,many=True).data)
        context['vehicles_s']=vehicles_s



        
        work_shifts =[]
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s



        
        anbar_products =[]
        context['anbar_products']=anbar_products
        anbar_products_s=json.dumps(AnbarProductSerializer(anbar_products,many=True).data)
        context['anbar_products_s']=anbar_products_s


        services =[]
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s

        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+'.add_vehicle'):
            context['add_vehicle_form']=AddVehicleForm()
            from .enums import VehicleTypeEnum,VehicleColorEnum,VehicleBrandEnum
            context['vehicle_types']=(i[0] for i in VehicleTypeEnum.choices)
            context['vehicle_colors']=(i[0] for i in VehicleColorEnum.choices)
            context['brand_names']=(i[0] for i in VehicleBrandEnum.choices)
            context['drivers']=DriverRepo(request=request).list()
        return render(request,TEMPLATE_ROOT+"report.html",context) 

    
class VehicleView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        vehicle =VehicleRepo(request=request).vehicle(*args, **kwargs)
        context[WIDE_LAYOUT]=True
        context['vehicle']=vehicle 

        if vehicle is None:
                    from core.views import MessageView
                    mv=MessageView()
                    return mv.get(request=request,title="پیدا نشد")
        
        context.update(VehicleContext(request=request,vehicle=vehicle))
        maintenances=MaintenanceRepo(request=request).list(vehicle_id=vehicle.id)
        context['maintenances']=maintenances
        maintenances_s=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
        context['maintenances_s']=maintenances_s

        vehicle_statuses=vehicle.vehiclestatus_set.all().order_by('-status_datetime')
        context['vehicle_statuses']=vehicle_statuses
        vehicle_statuses_s=json.dumps(VehicleStatusSerializer(vehicle_statuses,many=True).data)
        context['vehicle_statuses_s']=vehicle_statuses_s


        services=vehicle.service_set.all().order_by('shift_date')
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s


         


        work_shifts =WorkShiftRepo(request=request).list(vehicle_id=vehicle.id)
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s




        return render(request,TEMPLATE_ROOT+"vehicle.html",context) 
  
    
class VehicleStatusesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context[WIDE_LAYOUT]=True 

        vehicle_statuses=VehicleStatusRepo(request=request).last_statuses(*args, **kwargs)
        context['vehicle_statuses']=vehicle_statuses
        vehicle_statuses_s=json.dumps(VehicleStatusSerializer(vehicle_statuses,many=True).data)
        context['vehicle_statuses_s']=vehicle_statuses_s
        return render(request,TEMPLATE_ROOT+"vehicle-statuses.html",context) 

 
class VehicleStatusesExcelView(View):
    def post(self,request,*args, **kwargs):
        context={}
        from utility.constants import FAILED,SUCCEED
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        vehicle_statuses_excel_form=VehicleStatusesExcelForm(request.POST)
        if vehicle_statuses_excel_form.is_valid():
            log=333
            cd=vehicle_statuses_excel_form.cleaned_data
            vehicle_statuses=VehicleStatusRepo(request=request).last_statuses(**cd)
        now=PersianCalendar().date
        
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        from utility.templatetags.to_normal_number import to_normal_number
        leolog(vehicle_statuses=vehicle_statuses)
        for i,vehicle_status in enumerate(vehicle_statuses,start=1):
            line={
                'row':i,
                'vehicle_code':vehicle_status.vehicle.vehicle_code,      
                'vehicle':vehicle_status.vehicle.title,      
                'datetime':PersianCalendar().from_gregorian(vehicle_status.status_datetime)[:10],      
                'location':vehicle_status.location,  
                'kilometer':vehicle_status.kilometer,   
                'hour':vehicle_status.hour,   
                'motor':vehicle_status.motor,   
                'ziroband':vehicle_status.ziroband,   
                'cabin':vehicle_status.cabin,   
                'compress':vehicle_status.compress,   
                'hydrolic':vehicle_status.hydrolic,   
                'pakat':vehicle_status.pakat,   
                'cooler':vehicle_status.cooler,   
                'heater':vehicle_status.heater,   
                'gear_box':vehicle_status.gear_box,   
                'wiring':vehicle_status.wiring,   
                'light':vehicle_status.light,   
                'description':vehicle_status.description,      
            }
            lines.append(line)
        headers=['ردیف',
                 'کد',
                 'دستگاه',
                 'تاریخ',
                 'مکان',
                 'کیلومتر',
                 'ساعت',
                 'موتور',
                 'زیروبند',
                 'کابین',
                 'کمپرس',
                 'هیدرولیک',
                 'پاکت',
                 'کولر',
                 'بخاری',
                 'گیربکس',
                 'سیم کشی', 
                 'لامپ',
                 'توضیحات'
        ]
                
        from utility.excel import ReportWorkBook,get_style
        report_work_book=ReportWorkBook(origin_file_name=f'transport.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        # sheet1=ReportSheet(
        #     data=lines,
        #     start_row=3,
        #     start_col=1,
        #     table_has_header=False,
        #     table_headers=None,
        #     style=style,
        #     sheet_name='links',
            
        # )
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='Statuses',
        )
            
        file_name=f"""Phoenix Transport Statuses {date.replace('/','').replace(':','')}.xlsx"""
        from django.http import HttpResponse
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response

      

class VehicleStatusView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 

        vehicle_status=VehicleStatusRepo(request=request).vehicle_status(*args, **kwargs)
        if vehicle_status is None:
            from core.views import MessageView
            mv=MessageView()
            return mv.get(request=request,title="پیدا نشد")

        
        vehicle=vehicle_status.vehicle
        context.update(PageContext(request=request,page=vehicle))
        context['vehicle']=vehicle
        context['vehicle_status']=vehicle_status
        vehicle_status_s=json.dumps(VehicleStatusSerializer(vehicle_status,many=False).data)
        context['vehicle_status_s']=vehicle_status_s
        return render(request,TEMPLATE_ROOT+"vehicle-status.html",context) 
  

class VehicleEventsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        context[WIDE_LAYOUT]=True 

        vehicle_events=VehicleEventRepo(request=request).list()
        context['vehicle_events']=vehicle_events
        vehicle_events_s=json.dumps(VehicleEventSerializer(vehicle_events,many=True).data)
        context['vehicle_events_s']=vehicle_events_s

        return render(request,TEMPLATE_ROOT+"vehicle-events.html",context) 
  
    
class NewOilingMaintenanceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        if request.user.has_perm(APP_NAME+'.add_maintenance'):
            context.update(AddMaintenanceContext(request=request))
            context['add_oiling_maintenance_form']=AddOilingMaintenanceForm()
            context['oil_types']=(i[0] for i in OilTypeEnum.choices)
        return render(request,TEMPLATE_ROOT+"new-oiling-maintenance.html",context) 

    
class MaintenanceInvoicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        maintenance_invoices =MaintenanceInvoiceRepo(request=request).list(*args, **kwargs)
        context['maintenance_invoices']=maintenance_invoices
        maintenance_invoices_s=json.dumps(MaintenanceInvoiceSerializer(maintenance_invoices,many=True).data)
        context['maintenance_invoices_s']=maintenance_invoices_s
 
        context[WIDE_LAYOUT]=False
        if request.user.has_perm(APP_NAME+'.add_maintenanceinvoice'):
            context['add_maintenance_invoice_form']=AddMaintenanceInvoiceForm()
        return render(request,TEMPLATE_ROOT+"maintenance-invoices.html",context) 
    
    
class MaintenanceInvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        maintenance_invoice =MaintenanceInvoiceRepo(request=request).maintenance_invoice(*args, **kwargs)
        context[WIDE_LAYOUT]=False
        context['maintenance_invoice']=maintenance_invoice
        from accounting.views import InvoiceContext
        context.update(InvoiceContext(request=request,invoice=maintenance_invoice))
        return render(request,TEMPLATE_ROOT+"maintenance-invoice.html",context) 
    

class MaintenancesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        maintenances =MaintenanceRepo(request=request).list(*args, **kwargs)
        context['maintenances']=maintenances
        maintenances_s=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
        context['maintenances_s']=maintenances_s
 
        context[WIDE_LAYOUT]=False
        if request.user.has_perm(APP_NAME+'.add_maintenance'):
            context.update(AddMaintenanceContext(request=request))
        return render(request,TEMPLATE_ROOT+"maintenances.html",context) 
    
    
class MaintenanceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        maintenance =MaintenanceRepo(request=request).maintenance(*args, **kwargs)
        if maintenance is None:
            from core.views import MessageView
            mv=MessageView()
            return mv.get(request=request,title="پیدا نشد")
        context[WIDE_LAYOUT]=True
        context['maintenance']=maintenance 
        maintenance_s=json.dumps(MaintenanceSerializer(maintenance,many=False).data)
        context['maintenance_s']=maintenance_s 
        context.update(PageContext(request=request,page=maintenance))


        
        invoices=maintenance.invoices.order_by('-event_datetime')
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices']=invoices
        context['invoices_s']=invoices_s




        
        invoice_lines=maintenance.all_invocie_lines().order_by('invoice_line_item__title')
        invoice_lines_s=json.dumps(InvoiceLineWithInvoiceSerializer(invoice_lines,many=True).data)
        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=invoice_lines_s

        if request.user.has_perm('accounting.add_invoice'):
            context['add_invoice_to_maintenance_form']=AddInvoiceToMaintenanceForm()
            context['add_invoice_form']=AddInvoiceForm()
            context.update(AddInvoiceContext(request=request))

        return render(request,TEMPLATE_ROOT+"maintenance.html",context) 

    
class OilingMaintenanceDetailsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        oiling_maintenance_details =OilingMaintenanceDetailRepo(request=request).list(*args, **kwargs)
        
        context[WIDE_LAYOUT]=True
        context['oiling_maintenance_details']=oiling_maintenance_details 
        oiling_maintenance_details_s=json.dumps(OilingMaintenanceDetailSerializer(oiling_maintenance_details,many=True).data)
        context['oiling_maintenance_details_s']=oiling_maintenance_details_s 

        context['expand_oiling_maintenance_details']=True
          

        if request.user.has_perm('accounting.add_oilingmaintenancedetail'):
            context.update(AddOilingMaintenanceDetailContext(request=request))
        return render(request,TEMPLATE_ROOT+"oiling-maintenance-details.html",context) 
    

class OilingMaintenancesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        oiling_maintenances =OilingMaintenanceRepo(request=request).list(*args, **kwargs)
        context['oiling_maintenances']=oiling_maintenances
        oiling_maintenances_s=json.dumps(OilingMaintenanceSerializer(oiling_maintenances,many=True).data)
        context['oiling_maintenances_s']=oiling_maintenances_s
 
        context[WIDE_LAYOUT]=False
        if request.user.has_perm(APP_NAME+'.add_oilingmaintenance'):
            context.update(AddOilingMaintenanceContext(request=request))
        return render(request,TEMPLATE_ROOT+"oiling-maintenances.html",context) 

        
class OilingMaintenanceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        oiling_maintenance =OilingMaintenanceRepo(request=request).oiling_maintenance(*args, **kwargs)
        if oiling_maintenance is None:
            from core.views import MessageView
            mv=MessageView()
            return mv.get(request=request,title="پیدا نشد")
        context[WIDE_LAYOUT]=True
        context['oiling_maintenance']=oiling_maintenance 
        context['expand_oiling_maintenance_details']=True 
        maintenance=oiling_maintenance
        context['maintenance']=maintenance 
        maintenance_s=json.dumps(MaintenanceSerializer(maintenance,many=False).data)
        context['maintenance_s']=maintenance_s 
        context.update(PageContext(request=request,page=maintenance))


        
        invoices=maintenance.invoices.order_by('-event_datetime')
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices']=invoices
        context['invoices_s']=invoices_s




        
        invoice_lines=maintenance.all_invocie_lines().order_by('invoice_line_item__title')
        invoice_lines_s=json.dumps(InvoiceLineWithInvoiceSerializer(invoice_lines,many=True).data)
        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=invoice_lines_s
        
        oiling_maintenance_details=oiling_maintenance.oilingmaintenancedetail_set.all()
        oiling_maintenance_details_s=json.dumps(OilingMaintenanceDetailSerializer(oiling_maintenance_details,many=True).data)
        context['oiling_maintenance_details']=oiling_maintenance_details
        context['oiling_maintenance_details_s']=oiling_maintenance_details_s

        if request.user.has_perm('accounting.add_invoice'):
            context['add_invoice_to_maintenance_form']=AddInvoiceToMaintenanceForm()
            context['add_invoice_form']=AddInvoiceForm()
            context.update(AddInvoiceContext(request=request))

        if request.user.has_perm('accounting.add_oilingmaintenancedetail'):
            context.update(AddOilingMaintenanceDetailContext(request=request))
        return render(request,TEMPLATE_ROOT+"oiling-maintenance.html",context) 

    
class OilingMaintenancePrintView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        oiling_maintenance =OilingMaintenanceRepo(request=request).oiling_maintenance(*args, **kwargs)
        if oiling_maintenance is None:
            from core.views import MessageView
            mv=MessageView()
            return mv.get(request=request,title="پیدا نشد")
        context[WIDE_LAYOUT]=True
        context['oiling_maintenance']=oiling_maintenance 
        maintenance=oiling_maintenance
        context['NO_FOOTER']=True 
        context['NO_NAVBAR']=True 
        context['maintenance']=maintenance 
        maintenance_s=json.dumps(MaintenanceSerializer(maintenance,many=False).data)
        context['maintenance_s']=maintenance_s 
        context.update(PageContext(request=request,page=maintenance))
        invoices=maintenance.invoices.order_by('-event_datetime')
        invoices_s=json.dumps(InvoiceSerializer(invoices,many=True).data)
        context['invoices']=invoices
        context['invoices_s']=invoices_s




        
        invoice_lines=maintenance.all_invocie_lines().order_by('invoice_line_item__title')
        invoice_lines_s=json.dumps(InvoiceLineWithInvoiceSerializer(invoice_lines,many=True).data)
        context['invoice_lines']=invoice_lines
        context['invoice_lines_s']=invoice_lines_s
        
        oiling_maintenance_details=oiling_maintenance.oilingmaintenancedetail_set.all()
        oiling_maintenance_details_s=json.dumps(OilingMaintenanceDetailSerializer(oiling_maintenance_details,many=True).data)
        context['oiling_maintenance_details']=oiling_maintenance_details
        context['oiling_maintenance_details_s']=oiling_maintenance_details_s

        if request.user.has_perm('accounting.add_invoice'):
            context['add_invoice_to_maintenance_form']=AddInvoiceToMaintenanceForm()
            context['add_invoice_form']=AddInvoiceForm()
            context.update(AddInvoiceContext(request=request))

        if request.user.has_perm('accounting.add_oilingmaintenancedetail'):
            context.update(AddOilingMaintenanceDetailContext(request=request))
        return render(request,TEMPLATE_ROOT+"oiling-maintenance-print.html",context) 
            

class ServiceMansView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service_mans =ServiceManRepo(request=request).list(*args, **kwargs)
        context['service_mans']=service_mans
        service_mans_s=json.dumps(ServiceManSerializer(service_mans,many=True).data)
        context['service_mans_s']=service_mans_s
 
        context[WIDE_LAYOUT]=False
        if request.user.has_perm(APP_NAME+'.add_serviceman'):
            context['add_service_man_form']=AddServiceManForm()
        return render(request,TEMPLATE_ROOT+"service-mans.html",context) 

 
class OilingMaintenanceDetailsExcelView(View):
    def post(self,request,*args, **kwargs):
        context={}
        from utility.constants import FAILED,SUCCEED
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        oiling_maintenance_details_excel_form=OilingMaintenanceDetailsExcelForm(request.POST)
        if oiling_maintenance_details_excel_form.is_valid():
            log=333
            cd=oiling_maintenance_details_excel_form.cleaned_data
            oiling_maintenance_details=OilingMaintenanceDetailRepo(request=request).list(**cd)
 
        now=PersianCalendar().date
        
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        from utility.templatetags.to_normal_number import to_normal_number
        for i,oiling_maintenance_detail in enumerate(oiling_maintenance_details,start=1):
            line={
                'row':i,
                'vehicle':oiling_maintenance_detail.vehicle.title,      
                'datetime':oiling_maintenance_detail.oiling_maintenance.persian_event_datetime()[:10],      
                'service_man':oiling_maintenance_detail.oiling_maintenance.service_man.person_account.person.full_name,      
                'filter_type':oiling_maintenance_detail.filter_type,      
                'filter_action':oiling_maintenance_detail.filter_action,      
                'count':oiling_maintenance_detail.count,      
                'cost':oiling_maintenance_detail.cost,      
                'description':oiling_maintenance_detail.description,      
            }
            lines.append(line)
        headers=['ردیف',
                 'ماشین',
                 'تاریخ',
                 'سرویسکار',
                 'فیلتر',
                 'سرویس',
                 'تعداد', 
                 'برآورد هزینه',
                 'توضیحات'
        ]
                
        from utility.excel import ReportWorkBook,get_style
        report_work_book=ReportWorkBook(origin_file_name=f'transport.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        # sheet1=ReportSheet(
        #     data=lines,
        #     start_row=3,
        #     start_col=1,
        #     table_has_header=False,
        #     table_headers=None,
        #     style=style,
        #     sheet_name='links',
            
        # )
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            sheet_name='OilingMaintenanceDetails',
        )
            
        file_name=f"""Phoenix OilingMaintenanceDetails {date.replace('/','').replace(':','')}.xlsx"""
        from django.http import HttpResponse
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response

    
class ServiceManView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        service_man =ServiceManRepo(request=request).service_man(*args, **kwargs)
        context[WIDE_LAYOUT]=False
        context['service_man']=service_man
        if service_man is None:

            mv=MessageView()
            return mv.get(request=request,title="پیدا نشد")

        maintenances =MaintenanceRepo(request=request).list(service_man_id=service_man.id)
        context['maintenances']=maintenances
        maintenances_s=json.dumps(MaintenanceSerializer(maintenances,many=True).data)
        context['maintenances_s']=maintenances_s
 

        services=service_man.service_set.all().order_by('shift_date')
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s
        context[WIDE_LAYOUT]=True


        return render(request,TEMPLATE_ROOT+"service-man.html",context) 

    
class NewKarkerdView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        if not request.user.has_perm(APP_NAME+".add_karkerd"):
            
            mv=MessageView()
            return mv.get(request=request,title="دسترسی غیر مجاز")

        context['add_karkerd_form']=AddKarkerdForm()

        vehicles =VehicleRepo(request=request).list()
        context['vehicles']=vehicles
        vehicles_s=json.dumps(VehicleSerializer(vehicles,many=True).data)
        context['vehicles_s']=vehicles_s

        from attachments.repo import AreaRepo
        areas=AreaRepo(request=request).list()
        context['areas']=areas

        from projectmanager.views import ProjectRepo
        projects=ProjectRepo(request=request).list()
        context['projects']=projects
 
        drivers=DriverRepo(request=request).list()
        context['drivers']=drivers

        return render(request,TEMPLATE_ROOT+"new-karkerd.html",context) 


class NewWorkShiftView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        if not request.user.has_perm(APP_NAME+".add_workshift"):
            mv=MessageView()
            return mv.get(request=request,title="دسترسی غیر مجاز")

        context['add_work_shift_form']=AddKarkerdForm()
 
        vehicles =VehicleRepo(request=request).list(*args, **kwargs)
        context['vehicles']=vehicles

        
        from .enums import OilActionEnum
        drivers =DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        context['oil_types']=(i[0] for i in OilTypeEnum.choices)
        context['oil_actions']=(i[0] for i in OilActionEnum.choices)
        context['filter_types']=(i[0] for i in FilterTypeEnum.choices)
        context['filter_actions']=(i[0] for i in FilterActionEnum.choices)
        context['tavaghof_causes']=(i[0] for i in TavaghofCausesEnum.choices)

        return render(request,TEMPLATE_ROOT+"new-work-shift.html",context) 


class WorkShiftView(View):
    def get(self,request,*args, **kwargs):
        work_shift =WorkShiftRepo(request=request).work_shift(*args, **kwargs)
        if work_shift is None:
            mv=MessageView()
            return mv.get(request=request,title="وجود ندارد")

 
        context=getContext(request=request)

        

 
        context['work_shift']=work_shift

        oil_services =work_shift.oilservice_set.all()
        context['oil_services']=oil_services
        oil_services_s=json.dumps(OilServiceSerializer(oil_services,many=True).data)
        context['oil_services_s']=oil_services_s





        filter_services =work_shift.filterservice_set.all()
        context['filter_services']=filter_services
        filter_services_s=json.dumps(FilterServiceSerializer(filter_services,many=True).data)
        context['filter_services_s']=filter_services_s





        products =work_shift.product_set.all()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s



        context['expand_oil_services']=True
        context[WIDE_LAYOUT]=True

        return render(request,TEMPLATE_ROOT+"work-shift.html",context) 


class WorkShiftsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
 
        work_shifts =WorkShiftRepo(request=request).list(*args, **kwargs).order_by('-start_hour').order_by('-shift_date')
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s



         
        context['expand_work_shifts']=True
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"work-shifts.html",context) 


class AnbarProductView(View):
    def get(self,request,*args, **kwargs):
        work_shift =WorkShiftRepo(request=request).work_shift(*args, **kwargs)
        if work_shift is None:
            mv=MessageView()
            return mv.get(request=request,title="وجود ندارد")

 
        context=getContext(request=request)

        

 
        context['work_shift']=work_shift

        oil_services =work_shift.oilservice_set.all()
        context['oil_services']=oil_services
        oil_services_s=json.dumps(OilServiceSerializer(oil_services,many=True).data)
        context['oil_services_s']=oil_services_s





        filter_services =work_shift.filterservice_set.all()
        context['filter_services']=filter_services
        filter_services_s=json.dumps(FilterServiceSerializer(filter_services,many=True).data)
        context['filter_services_s']=filter_services_s





        products =work_shift.product_set.all()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s



        context['expand_oil_services']=True
        context[WIDE_LAYOUT]=True

        return render(request,TEMPLATE_ROOT+"anbar-product.html",context) 


class AnbarProductsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
 
        anbar_products =AnbarProductRepo(request=request).list(*args, **kwargs) 
        context['anbar_products']=anbar_products
        anbar_products_s=json.dumps(AnbarProductSerializer(anbar_products,many=True).data)
        context['anbar_products_s']=anbar_products_s



         
        context['expand_anbar_products']=True
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"anbar-products.html",context) 


class ServiceView(View):
    def get(self,request,*args, **kwargs):
      
 
        context=getContext(request=request)

        
 
        service =ServiceRepo(request=request).service(*args, **kwargs)
        context['service']=service
        service_s=json.dumps(ServiceSerializer(service,many=False).data)
        context['service_s']=service_s


  
        context[WIDE_LAYOUT]=True

        return render(request,TEMPLATE_ROOT+"service.html",context) 


class ServicesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
 
        services =ServiceRepo(request=request).list(*args, **kwargs) 
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s



         
        context['expand_services']=True
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"services.html",context) 

 

class NewServiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 


        drivers =DriverRepo(request=request).list(*args, **kwargs)
        context['drivers']=drivers
        vehicles =VehicleRepo(request=request).list(*args, **kwargs)
        context['vehicles']=vehicles
        service_mans =ServiceManRepo(request=request).list(*args, **kwargs)
        context['service_mans']=service_mans
         
        context['filter_types']=(i[0] for i in FilterTypeEnum.choices)
        context['oil_types']=(i[0] for i in OilTypeEnum.choices)
        context['expand_services']=True

        
        services =[]
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s
        
        
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"new-service.html",context) 

 
class VehiclesExcelView(View):
    def post(self,request,*args, **kwargs):
        context={}
        from utility.constants import FAILED,SUCCEED
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        vehicles_excel_form=VehiclesExcelForm(request.POST)
        if vehicles_excel_form.is_valid():
            log=333
            cd=vehicles_excel_form.cleaned_data
            vehicles=VehicleRepo(request=request).list(**cd)
 
        now=PersianCalendar().date
        
        date=PersianCalendar().from_gregorian(now)
        lines=[]
        from utility.templatetags.to_normal_number import to_normal_number
        for i,vehicle in enumerate(vehicles,start=1):
            line={
                'row':i,
                'id':vehicle.id,
                'vehicle_code':vehicle.vehicle_code,   
                'vehicle_type':vehicle.vehicle_type,      
                'title':vehicle.title,   
                'year':vehicle.year,   
                'plaque':vehicle.plaque,   
                'vehicle_color':vehicle.vehicle_color,   
                'kilometer':vehicle.kilometer,   
                'description':vehicle.description,      
            }
            lines.append(line)
 
        headers=['ردیف',
                 'شناسه',
                 'کد',
                 'نوع',
                 'ماشین',
                 'سال',
                 'پلاک',
                 'رنگ',
                 'کیلومتر',
                 'توضیحات'
        ]
                
        from utility.excel import ReportWorkBook,get_style
        report_work_book=ReportWorkBook(origin_file_name=f'transport.xlsx')
        style=get_style(font_name='B Koodak',size=12,bold=False,color='FF000000',start_color='FFFFFF',end_color='FF000000')
        # sheet1=ReportSheet(
        #     data=lines,
        #     start_row=3,
        #     start_col=1,
        #     table_has_header=False,
        #     table_headers=None,
        #     style=style,
        #     sheet_name='links',
            
        # )
        
        start_row=3
        report_work_book.add_sheet(
            data=lines,
            start_row=start_row,
            table_has_header=False,
            table_headers=headers,
            style=style,
            # sheet_name='vehicles',
        )
            
        file_name=f"""Phoenix Transport vehicles {date.replace('/','').replace(':','')}.xlsx"""
        from django.http import HttpResponse
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response.AppendHeader("Content-Type", "application/vnd.ms-excel");
        response["Content-disposition"]=f"attachment; filename={file_name}"
        report_work_book.work_book.save(response)
        report_work_book.work_book.close()
        return response

      

class DriverView(View):
    def get(self,request,*args, **kwargs):
      
 
        context=getContext(request=request)

         

        driver =DriverRepo(request=request).driver(*args, **kwargs)
        context['driver']=driver
        driver_s=json.dumps(DriverSerializer(driver,many=False).data)
        context['driver_s']=driver_s
  
        context[WIDE_LAYOUT]=True


 
        services =ServiceRepo(request=request).list(driver_id=driver.id)
        context['services']=services
        services_s=json.dumps(ServiceSerializer(services,many=True).data)
        context['services_s']=services_s


        work_shifts =WorkShiftRepo(request=request).list(driver_id=driver.id).order_by('-start_hour').order_by('-shift_date')
        context['work_shifts']=work_shifts
        work_shifts_s=json.dumps(WorkShiftSerializer(work_shifts,many=True).data)
        context['work_shifts_s']=work_shifts_s



         



        return render(request,TEMPLATE_ROOT+"driver.html",context) 


class DriversView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
 
        drivers =DriverRepo(request=request).list(*args, **kwargs) 
        context['drivers']=drivers
        drivers_s=json.dumps(DriverSerializer(drivers,many=True).data)
        context['drivers_s']=drivers_s



         
        context['expand_drivers']=True
        context[WIDE_LAYOUT]=True
        return render(request,TEMPLATE_ROOT+"drivers.html",context) 

 
