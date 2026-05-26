from rest_framework import serializers
from .models import OrganizationalUnit,Employee
from accounting.serializers import PersonAccountSerializer,PersonSerializer,FinancialEventSerializer,InvoiceLineSerializer,AccountBriefSerializer
 
class OrganizationalUnitSerializer(FinancialEventSerializer):
       person_account=AccountBriefSerializer()
       class Meta:
        model = OrganizationalUnit
        fields = ['id','full_title','title','person_account','thumbnail', 'get_absolute_url','get_edit_url','get_delete_url']
 
 
class EmployeeSerializer(FinancialEventSerializer):
       organizational_unit=OrganizationalUnitSerializer()
       person_account=PersonAccountSerializer()
       class Meta:
        model = Employee
        fields = ['id','person_account','job_title','organizational_unit','get_absolute_url','get_edit_url','get_delete_url']
 