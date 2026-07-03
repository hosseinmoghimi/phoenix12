from core.serializers import serializers
from .models import Vehicle,MaintenanceInvoice,ServiceMan,Maintenance
from accounting.serializers import PersonAccountSerializer,AccountBriefSerializer,InvoiceSerializer
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
        fields=['id', 'title','vehicle','kilometer','sum','service_man','persian_event_datetime','persian_end_datetime','persian_start_datetime','get_absolute_url',  'get_edit_url','get_delete_url']
 
 