from rest_framework import serializers
from .models import Table,Table,TableCustomer,Menu,MenuItem
from accounting.serializers import AccountBriefSerializer
from market.serializers import SupplierSerializer,ShopSerializer
 
 
class TableSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    class Meta:
        model=Table 
        fields=['id','table_no','title','supplier',  'get_absolute_url', 'get_edit_url','get_delete_url']
 

class TableCustomerSerializer(serializers.ModelSerializer):
    account=AccountBriefSerializer()
    table=TableSerializer()
    class Meta:
        model=TableCustomer 
        fields=['id','table','account',  'get_absolute_url', 'get_edit_url','get_delete_url']
 
class MenuSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    shops=ShopSerializer(many=True)
    class Meta:
        model=Menu
        fields=['id','title','supplier','shops', 'get_absolute_url', 'get_edit_url','get_delete_url']



class MenuItemSerializer(serializers.ModelSerializer):
    shop=ShopSerializer()
    class Meta:
        model=MenuItem
        fields=['id','shop','quantity']

