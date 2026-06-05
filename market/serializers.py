from core.serializers import serializers
from utility.serializers import RegionSerializer
from .models import ShopPackage,Shop,Supplier,Customer,CartItem,Shipper,CustomerGroup
from accounting.serializers import Category,Product,AccountBriefSerializer,PersonSerializer,PersonAccountSerializer





class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerGroup
        fields=['id','name','color', 'get_absolute_url', 'get_edit_url','get_delete_url']
 
 
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'title','unit_name','unit_price','thumbnail','get_market_absolute_url',  'get_edit_url','get_delete_url']
 

class ProductWithPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'available','title','unit_name','unit_price','thumbnail','get_market_absolute_url',  'get_edit_url','get_delete_url']
 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id', 'title','thumbnail','get_market_absolute_url',  'get_edit_url','get_delete_url']
 

class SupplierSerializer(serializers.ModelSerializer):
    person_account=PersonAccountSerializer()
    regions=RegionSerializer(many=True)
    class Meta:
        model=Supplier
        fields=['id','regions','person_account','full_name',  'get_absolute_url', 'get_edit_url','get_delete_url']
 
 
class ShopSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    supplier=SupplierSerializer()
    product=ProductSerializer()
    region=RegionSerializer()
    group=CustomerGroupSerializer()
    class Meta:
        model=Shop
        fields=['id','group','region','supplier','discount_percentage','unit_price','product','unit_name','quantity','available','persian_start_date','persian_end_date', 'get_absolute_url','get_edit_url','get_delete_url']
 

class CustomerSerializer(serializers.ModelSerializer):
    person_account=PersonAccountSerializer()
    regions=RegionSerializer(many=True)
    groups=CustomerGroupSerializer(many=True)
    class Meta:
        model=Customer
        fields=['id','regions','groups','full_name','person_account', 'get_absolute_url','get_edit_url','get_delete_url']
 

class ShipperSerializer(serializers.ModelSerializer):
    person_account=PersonAccountSerializer()
    regions=RegionSerializer(many=True)
    class Meta:
        model=Shipper
        fields=['id','regions','full_name','person_account', 'get_absolute_url','get_edit_url','get_delete_url']


class ShopPackageSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    class Meta:
        model=ShopPackage
        fields=['id','supplier', 'title','get_absolute_url','quantity','available','persian_start_date','persian_end_date',  'get_edit_url','get_delete_url']


class CartItemSerializer(serializers.ModelSerializer):
    shop=ShopSerializer()
    customer=CustomerSerializer()
    class Meta:
        model=CartItem
        fields=['id','row', 'shop','quantity','customer','persian_date_added']
 