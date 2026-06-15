from rest_framework import serializers
from .models import Table,Table,Menu
from accounting.serializers import AccountBriefSerializer
from market.serializers import SupplierSerializer,ShopSerializer
 
 
class TableSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    class Meta:
        model=Table 
        fields=['id','table_no','title','supplier',  'get_absolute_url', 'get_edit_url','get_delete_url']
  

class MenuSerializer(serializers.ModelSerializer):
    shops=ShopSerializer(many=True)
    class Meta:
        model=Menu
        fields=['id','title','shops', 'get_absolute_url', 'get_edit_url','get_delete_url']
 