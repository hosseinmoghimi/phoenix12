from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('report/',login_required(views.ReportView.as_view()),name="report"),
    path('get-report/',login_required(apis.GetReportApiw.as_view()),name="get_report"),

    path('add-vehicle/',login_required(apis.AddVehicleApi.as_view()),name="add_vehicle"),
    path('vehicles/',login_required(views.VehiclesView.as_view()),name="vehicles"),
    path('vehicle/<int:pk>/',login_required(views.VehicleView.as_view()),name="vehicle"),

    path('anbar-products',login_required(views.AnbarProductsView.as_view()),name="anbar_products"),
    path('anbar-product/<int:pk>/',login_required(views.AnbarProductView.as_view()),name="anbarproduct"),

    
    path('services',login_required(views.ServicesView.as_view()),name="services"),
    path('service/<int:pk>/',login_required(views.ServiceView.as_view()),name="service"),

    
    path('drivers/',login_required(views.VehiclesView.as_view()),name="drivers"),
    path('driver/<int:pk>/',login_required(views.VehicleView.as_view()),name="driver"),

    path('add-oiling-maintenance/',login_required(apis.AddOilingMaintenanceApi.as_view()),name="add_oiling_maintenance"),
    path('new-oiling-maintenance/',login_required(views.NewOilingMaintenanceView.as_view()),name="new_oiling_maintenance"),

    path('add-invoice-to-maintenance/',login_required(apis.AddInvoiceToMaintenanceApi.as_view()),name="add_invoice_to_maintenance"),

    
    path('add-invoice/',login_required(apis.AddInvoiceApi.as_view()),name="add_invoice"),
  
    path('maintenances/',login_required(views.MaintenancesView.as_view()),name="maintenances"),
    path('oiling_maintenance_details_excel/',login_required(views.OilingMaintenanceDetailsExcelView.as_view()),name="oiling_maintenance_details_excel"),
    path('vehicle-statuses-excel/',login_required(views.VehicleStatusesExcelView.as_view()),name="vehicle_statuses_excel"),
    path('maintenance/<int:pk>/',login_required(views.MaintenanceView.as_view()),name="maintenance"),
    path('add-maintenance/',login_required(apis.AddMaintenanceApi.as_view()),name="add_maintenance"),

    path('work-shifts/',login_required(views.WorkShiftsView.as_view()),name="work_shifts"),
    path('new-work-shift/',login_required(views.NewWorkShiftView.as_view()),name="new_work_shift"),
    path('add-work-shift/',login_required(apis.AddWorkShiftApi.as_view()),name="add_work_shift"),
    path('work-shift/<int:pk>/',login_required(views.WorkShiftView.as_view()),name="workshift"),

    
    path('new-karkerd/',login_required(views.NewKarkerdView.as_view()),name="new_karkerd"),
    path('add-karkerd/',login_required(apis.AddKarkerdApi.as_view()),name="add_karkerd"),

    path('add-oiling-maintenance/',login_required(apis.AddOilingMaintenanceApi.as_view()),name="add_oilingmaintenance"),

    path('service-mans/',login_required(views.ServiceMansView.as_view()),name="service_mans"),
    path('service-man/<int:pk>/',login_required(views.ServiceManView.as_view()),name="serviceman"),
    path('add-service-man/',login_required(apis.AddServiceManApi.as_view()),name="add_service_man"),


    path('vehicle-events/',login_required(views.VehicleEventsView.as_view()),name="vehicle_events"),
    path('karkerd/<int:pk>/',login_required(views.ServiceManView.as_view()),name="karkerd"),
    path('tavaghof/<int:pk>/',login_required(views.ServiceManView.as_view()),name="tavaghof"),


    path('vehicle-statuses/',login_required(views.VehicleStatusesView.as_view()),name="vehicle_statuses"),
    path('vehicle-status/<int:pk>/',login_required(views.VehicleStatusView.as_view()),name="vehiclestatus"),



]
