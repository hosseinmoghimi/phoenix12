from rest_framework import serializers
from .models import WareHouse,ProductInWareHouse,WareHouseSheet,WareHouseSheetSignature,WareHouseSheetLabel
from accounting.serializers import PersonAccountSerializer,InvoiceLineWithInvoiceSerializer,ProductSerializer
from authentication.serializers import PersonSerializer
from organization.serializers import EmployeeSerializer,OrganizationalUnitSerializer

class WareHouseSerializer(serializers.ModelSerializer):
       person_account=PersonAccountSerializer()
       class Meta:
              model = WareHouse
              fields = ['id','name','thumbnail','person_account', 'get_absolute_url','get_edit_url','get_delete_url']
  
class WareHouseSheetSerializer(serializers.ModelSerializer):
       invoice_line=InvoiceLineWithInvoiceSerializer()
       warehouse=WareHouseSerializer()
       organizational_unit=OrganizationalUnitSerializer()
       employee=EmployeeSerializer()
       class Meta:
              model = WareHouseSheet
              fields = ['id','shelf','status_color','status','type','organizational_unit','sum','col','row','invoice_line','direction','warehouse','persian_date_added','employee', 'get_absolute_url','get_edit_url','get_delete_url']
  
class WareHouseSheetSignatureSerializer(serializers.ModelSerializer):
       warehouse_sheet=WareHouseSheetSerializer()
       employee=EmployeeSerializer()
       class Meta:
              model = WareHouseSheetSignature
              fields = ['id', 'warehouse_sheet','status_color','status','description','persian_date_added','employee', 'get_edit_url','get_delete_url']
  
class WareHouseSheetLabelSerializer(serializers.ModelSerializer):
       warehouse_sheet=WareHouseSheetSerializer()
       class Meta:
              model = WareHouseSheetLabel
              fields = ['id', 'warehouse_sheet','label','serial_no','description','persian_date_added','get_edit_url','get_absolute_url','get_delete_url']
  
class ProductInWareHouseSerializer(serializers.ModelSerializer):
       product=ProductSerializer()
       warehouse=WareHouseSerializer()
       class Meta:
              model = ProductInWareHouse
              fields = ['id','product','warehouse','quantity','unit_name']
  