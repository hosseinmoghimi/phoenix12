from rest_framework import serializers
from .models import Table,Menu,Order
from accounting.serializers import AccountBriefSerializer
from market.serializers import SupplierSerializer,ShopSerializer
 
 
class TableSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    class Meta:
        model=Table 
        fields=['id','table_no','color','status','title','supplier',  'get_absolute_url', 'get_edit_url','get_delete_url']
  

class MenuSerializer(serializers.ModelSerializer):
    shops=ShopSerializer(many=True)
    class Meta:
        model=Menu
        fields=['id','title','shops', 'get_absolute_url', 'get_edit_url','get_delete_url']
 

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['id','status', 'get_absolute_url', 'get_edit_url','get_delete_url']
 