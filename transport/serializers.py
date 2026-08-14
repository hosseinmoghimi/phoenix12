from core.serializers import serializers
from .models import Vehicle,MaintenanceInvoice,ServiceMan,Maintenance,OilingMaintenance,OilingMaintenanceDetail,Driver
from accounting.serializers import PersonAccountSerializer,AccountBriefSerializer,InvoiceSerializer


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
 
 
  
class OilingMaintenanceSerializer(serializers.ModelSerializer):
    vehicle=VehicleSerializer()
    service_man=ServiceManSerializer()
    class Meta:
        model=OilingMaintenance
        fields=['id', 'title','hour','vehicle','kilometer','sum','service_man','persian_event_datetime','persian_end_datetime','persian_start_datetime','get_absolute_url',  'get_edit_url','get_delete_url']
 
 
class OilingMaintenanceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=OilingMaintenanceDetail
        fields=['id', 'filter_type','filter_action','count','description','cost', 'get_edit_url','get_delete_url']
 
 