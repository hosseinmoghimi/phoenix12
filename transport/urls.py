from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.IndexView.as_view()),name="index"),
    path('settings/',login_required(views.IndexView.as_view()),name="settings"),
    path('vehicles/',login_required(views.VehiclesView.as_view()),name="vehicles"),
    path('vehicle/<int:pk>/',login_required(views.VehicleView.as_view()),name="vehicle"),
    path('add-vehicle/',login_required(apis.AddVehicleApi.as_view()),name="add_vehicle"),

    path('add-invoice-to-maintenance/',login_required(apis.AddInvoiceToMaintenanceApi.as_view()),name="add_invoice_to_maintenance"),

    
    path('add-invoice/',login_required(apis.AddInvoiceApi.as_view()),name="add_invoice"),
  
    path('maintenances/',login_required(views.MaintenancesView.as_view()),name="maintenances"),
    path('maintenance/<int:pk>/',login_required(views.MaintenanceView.as_view()),name="maintenance"),
    path('add-maintenance/',login_required(apis.AddMaintenanceApi.as_view()),name="add_maintenance"),

    path('service-mans/',login_required(views.ServiceMansView.as_view()),name="service_mans"),
    path('service-man/<int:pk>/',login_required(views.ServiceManView.as_view()),name="serviceman"),
    path('add-service-man/',login_required(apis.AddServiceManApi.as_view()),name="add_service_man"),



]
