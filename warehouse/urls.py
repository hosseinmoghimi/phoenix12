from .apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    
    path('',login_required(views.IndexView.as_view()),name="index"),  
    path('settings/',login_required(views.SettingsView.as_view()),name="settings"),  
    path('normalize_product_in_warehouse/',login_required(apis.NormalizeProductInWareHouseApi.as_view()),name="normalize_product_in_warehouse"),  

    path('warehouses/',login_required(views.WareHousesView.as_view()),name="warehouses"),  
    path('add-warehouse/',login_required(apis.AddWareHouseApi.as_view()),name="add_warehouse"),
    path('warehouse/<int:pk>/',login_required(views.WareHouseView.as_view()),name="warehouse"), 

    path('add-material-request/',login_required(views.AddMaterialRequestView.as_view()),name="add_material_request"), 
 

    path('warehouse-sheet-label/<int:pk>/',login_required(views.WareHouseSheetLabelView.as_view()),name="warehousesheetlabel"), 
    path('warehouse-sheet-labels/',login_required(views.WareHouseSheetLabelsView.as_view()),name="warehouse_sheet_labels"), 
    path('add-warehouse-sheet-label/',login_required(apis.AddWareHouseSheetLabelApi.as_view()),name="add_warehouse_sheet_label"), 
    path('add-warehouse-sheet-signature/',login_required(apis.AddWareHouseSheetSignatureApi.as_view()),name="add_warehouse_sheet_signature"), 
    
    path('warehouse_sheets/',login_required(views.WareHouseSheetsView.as_view()),name="warehouse_sheets"),  
    path('add_invoice_warehouse_sheets/',login_required(apis.AddInvoiceWareHouseSheetsApi.as_view()),name="add_invoice_warehouse_sheets"), 
    path('add_warehouse_sheet/',login_required(apis.AddWareHouseSheetApi.as_view()),name="add_warehouse_sheet"), 
    path('warehouse_sheet/<int:pk>/',login_required(views.WareHouseSheetView.as_view()),name="warehousesheet"), 

    path('product_in_warehouse/',login_required(apis.ProductInWareHouseApi.as_view()),name="product_in_warehouse"), 
 
     path('select_warehouse/',login_required(apis.SelectWareHouseApi.as_view()),name="select_warehouse"), 
 
]
