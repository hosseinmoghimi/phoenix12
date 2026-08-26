from core.serializers import serializers
from .models import OilService,Tavaghof,FilterService,Product,Vehicle,MaintenanceInvoice,WorkShift,VehicleStatus,ServiceMan,Maintenance,Driver
from accounting.serializers import PersonAccountSerializer,AccountBriefSerializer,InvoiceSerializer

from .models import VehicleEvent,Tavaghof


class DriverSerializer(serializers.ModelSerializer):
    person_account=PersonAccountSerializer()
    class Meta:
        model=Driver
        fields=['id','person_account', 'get_absolute_url',  'get_edit_url','get_delete_url']
  

class VehicleSerializer(serializers.ModelSerializer):
    owner=PersonAccountSerializer()
    class Meta:
        model=Vehicle
        fields=['id','owner', 'title','thumbnail','get_absolute_url',  'get_edit_url','get_delete_url']
  
class VehicleSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields=['id','vehicle_code','thumbnail',  'title', 'get_absolute_url']
  
 
class VehicleStatusSerializer(serializers.ModelSerializer):
    vehicle=VehicleSerializer()
    class Meta:
        model=VehicleStatus
        fields=['id','vehicle','hour','kilometer','persian_status_datetime','short_desc', 'get_absolute_url','get_edit_url','get_delete_url' ]
  
 
class TavaghofSerializer(serializers.ModelSerializer):
    vehicle=VehicleSerializer()
    class Meta:
        model=Tavaghof
        fields=['id','vehicle','project_name','area_name','vehicle_event_type','title','cause','persian_event_datetime','persian_start_datetime','persian_end_datetime','short_description', 'get_edit_url','get_delete_url','get_absolute_url' ]

      

class VehicleEventSerializer(serializers.ModelSerializer):
    vehicle=VehicleSerializer()
    class Meta:
        model=VehicleEvent
        fields=['id','vehicle','project_name','area_name','vehicle_event_type','title','persian_event_datetime','persian_start_datetime','persian_end_datetime','short_description', 'get_edit_url','get_delete_url','get_absolute_url' ]

        
class ServiceManSerializer(serializers.ModelSerializer):
    person_account=PersonAccountSerializer()
    class Meta:
        model=ServiceMan
        fields=['id', 'title','person_account','get_absolute_url',  'get_edit_url','get_delete_url']
 
  
class MaintenanceSerializer(serializers.ModelSerializer):
    vehicle=VehicleSerializer()
    service_man=ServiceManSerializer()
    class Meta:
        model=Maintenance
        fields=['id', 'title','hour','vehicle','kilometer','sum','service_man','persian_event_datetime','persian_end_datetime','persian_start_datetime','get_absolute_url',  'get_edit_url','get_delete_url']
  

class WorkShiftSerializer(serializers.ModelSerializer):
    vehicle=VehicleSerializer2()
    driver=DriverSerializer()
    class Meta:
        model=WorkShift
        fields=['id','vehicle_karkerd','start_hour','end_hour','vehicle_start_hour','vehicle_end_hour','location','bar','bar_count','shift','vehicle_code','vehicle','title','gasoil_liter','oil_liter','tavaghof','persian_shift_date','driver','get_absolute_url', 'get_edit_url','get_delete_url']

   
class FilterServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=FilterService
        fields=['id','cost','count','filter_type','filter_action','description']


   
class OilServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=OilService
        fields=['id','vehicle_hour','oil_action','oil_liter','oil_type','description','cost']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','unit_price','quantity','description']

   