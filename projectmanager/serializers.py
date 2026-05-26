from rest_framework import serializers
from .models import Project,RemoteClient,Ticket
from accounting.serializers import FinancialEventSerializer,InvoiceLineSerializer,BrandSerializer,ProductSerializer
from organization.serializers import OrganizationalUnitSerializer,PersonSerializer

class ProjectSerializer(FinancialEventSerializer):
       contractor=OrganizationalUnitSerializer()
       employer=OrganizationalUnitSerializer()
       class Meta:
        model = Project
        fields = ['id','percentage_completed','amount','weight','title','thumbnail','persian_start_datetime','persian_end_datetime','employer','contractor', 'get_absolute_url','get_edit_url','get_delete_url']
 

  
class ProjectSerializerForGuantt(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','title','get_status_color','color','start_datetime','end_datetime','status','amount','get_absolute_url','short_description','thumbnail','percentage_completed']


  
class TicketSerializer(serializers.ModelSerializer):
    project=ProjectSerializer()
    person=PersonSerializer()
    class Meta:
        model=Ticket
        fields=['id','title','get_status_color','persian_datetime_added','status','project','get_absolute_url','description','person','get_edit_url','get_delete_url']


  
class TicketWithChildrenSerializer(serializers.ModelSerializer):
    project=ProjectSerializer()
    person=PersonSerializer()
    class Meta:
        model=Ticket
        fields=['id','title','get_status_color','persian_datetime_added','status','project','get_absolute_url','description','person','get_edit_url','get_delete_url']



   
class RemoteClientSerializer(serializers.ModelSerializer):
    brand=BrandSerializer()
    product=ProductSerializer()
    class Meta:
        model=RemoteClient
        fields=['id','brand','product', 'name','get_project_absolute_url','get_project_title', 'get_absolute_url', 'get_edit_url','remote_ip','any_desk_address'
                ,'any_desk_password','username','password','identity','ssid','preshared_key','local_ip'
                ,'frequency','protocol','channel_width','adsl_username','adsl_password',
                'telephone','contact'] 
