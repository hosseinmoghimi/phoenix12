from rest_framework import serializers
from .models import Asset,Category,InvoiceLineItem,Account,Service,Product,InvoiceLine,Invoice,FinancialEvent,FinancialDocumentLine,InvoiceLineItemUnit
from .models import FinancialDocument,ProductSpecification,FinancialYear,PersonAccount,Cheque
from .models import BankAccount,Bank
from .models import Brand,PersonCategory
from authentication.serializers import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Person
        fields=['id','full_name','image','username','user_id','get_absolute_url','get_accounting_absolute_url', 'get_edit_url','get_delete_url']
 
class AccountSerializer(serializers.ModelSerializer):
       class Meta:
        model = Account
        fields = ['id','title','name','full_name','thumbnail','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']




class AccountSerializer(serializers.ModelSerializer):
       class Meta:
        model = Account
        fields = ['id','title','name','full_name','thumbnail','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']


class PersonCategorySerializer(serializers.ModelSerializer):
       account=AccountSerializer()
       class Meta:
        model = PersonCategory
        fields = ['id','title','count_of_accounts','account','code_length' , 'get_absolute_url','get_edit_url','get_delete_url']


class AssetSerializer(serializers.ModelSerializer):
       owner=PersonSerializer()
       class Meta:
        model = Asset
        fields = ['id','title','owner',  'get_absolute_url','get_edit_url','get_delete_url']


class BankSerializer(serializers.ModelSerializer):
       class Meta:
        model = Bank
        fields = ['id','name','get_absolute_url','get_edit_url','get_delete_url']


class BrandSerializer(serializers.ModelSerializer):
       class Meta:
        model = Brand
        fields = ['id','name','logo', 'get_absolute_url','get_edit_url','get_delete_url']


class InvoiceSerializer(serializers.ModelSerializer):
       bedehkar=AccountSerializer()
       bestankar=AccountSerializer()
       class Meta:
        model = Invoice
        fields = ['id','title','valid','balance','thumbnail','bedehkar','status' ,'bestankar','amount','shipping_fee','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']
 

class FinancialYearSerializer(serializers.ModelSerializer): 
    class Meta:
        model = FinancialYear
        fields = ['id','in_progress','name','status','persian_start_date','persian_end_date', 'get_absolute_url','get_edit_url','get_delete_url']


class FinancialEventSerializer(serializers.ModelSerializer):
       bedehkar=AccountSerializer()
       bestankar=AccountSerializer()
       class Meta:
        model = FinancialEvent
        fields = ['id','title','balance','bedehkar','thumbnail' ,'bestankar','amount','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']


class ChequeSerializer(serializers.ModelSerializer):
       bedehkar=AccountSerializer()
       bestankar=AccountSerializer()
       class Meta:
        model = Cheque
        fields = ['id','title','bedehkar' ,'bestankar','amount','persian_event_datetime','get_absolute_url','get_edit_url','get_delete_url']


class ProductSerializer(serializers.ModelSerializer):
       class Meta:
        model = Product
        fields = ['id','rop','title','class_title','model','thumbnail','unit_name','unit_price','barcode',  'get_absolute_url','get_edit_url','get_delete_url']
        # fields = ['id','name','get_market_absolute_url','thumbnail','barcode','unit_price', 'unit_name',  'get_absolute_url','get_edit_url','get_delete_url']


class ServiceSerializer(serializers.ModelSerializer):
       class Meta:
        model = Service
        fields = ['id','title','thumbnail','unit_name','unit_price','get_absolute_url','get_edit_url','get_delete_url']
        # fields = ['id','name','get_market_absolute_url','thumbnail','barcode','unit_price', 'unit_name',  'get_absolute_url','get_edit_url','get_delete_url']


class InvoiceLineItemSerializer(serializers.ModelSerializer):
       class Meta:
              model = InvoiceLineItem
              fields = ['id','title','model','brand_name','class_title','thumbnail','unit_name','unit_price',  'get_absolute_url','get_edit_url','get_delete_url']
        # fields = ['id','name','get_market_absolute_url','thumbnail','barcode','unit_price', 'unit_name',  'get_absolute_url','get_edit_url','get_delete_url']


class InvoiceLineSerializer(serializers.ModelSerializer):
       invoice_line_item=InvoiceLineItemSerializer()
       class Meta:
        model = InvoiceLine
        fields = ['id','status','unit_price','row','line_total','quantity','unit_name','description','discount','discount_percentage',  'invoice_line_item' , 'get_absolute_url','get_edit_url','get_delete_url']


class InvoiceLineWithInvoiceSerializer(serializers.ModelSerializer):
       invoice_line_item=InvoiceLineItemSerializer()
       invoice=InvoiceSerializer()
       class Meta:
        model = InvoiceLine
        fields = ['id','status','invoice','unit_price','row','line_total','quantity','unit_name','discount','discount_percentage',  'invoice_line_item' , 'get_absolute_url','get_edit_url','get_delete_url']

 

class InvoiceLineItemUnitSerializer(serializers.ModelSerializer):
    invoice_line_item=InvoiceLineItemSerializer()
    class Meta:
        model = InvoiceLineItemUnit
        fields = ['id','unit_name','percentage_tag','default','unit_price','coef','invoice_line_item','persian_date_added', 'get_edit_url','get_delete_url']
 

class InvoiceLineItemUnitBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItemUnit
        fields = ['id','unit_name','default','unit_price','coef','persian_date_added', 'get_edit_url','get_delete_url']
 
  
class AccountBriefSerializer(serializers.ModelSerializer):
       class Meta:
        model = Account
        fields = ['id','parent_id','full_name','thumbnail','title','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']


class FinancialDocumentSerializer(serializers.ModelSerializer):
       class Meta:
        model = FinancialDocument
        fields = ['id','title','balance','bedehkar','status','status_color','bestankar','get_absolute_url','get_edit_url','get_delete_url']


class CategorySerializer(serializers.ModelSerializer):
       class Meta:
        model = Category
        fields = ['id','title','thumbnail','full_title','priority','get_absolute_url','get_edit_url','get_delete_url']


class FinancialDocumentLineSerializer(serializers.ModelSerializer):
       financial_event=FinancialEventSerializer()
       financial_document=FinancialDocumentSerializer()
       account=AccountSerializer()
       class Meta:
        model = FinancialDocumentLine
        fields = ['id','account','rest','status_color','status','financial_document','amount','title','persian_date_time','balance','bedehkar','bestankar','financial_event', 'get_absolute_url','get_edit_url','get_delete_url']

class FinancialDocumentLineForPrintSerializer(serializers.ModelSerializer):
       class Meta:
        model = FinancialDocumentLine
        fields = ['id','rest','amount','title','persian_date_time','balance','bedehkar','bestankar','get_absolute_url','get_edit_url','get_delete_url']


class ProductSpecificationSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model = ProductSpecification
        fields = ['id','name','value','product', 'get_edit_url','get_delete_url']


class PersonAccountSerializer(serializers.ModelSerializer):
       person=PersonSerializer()
       person_category=PersonCategorySerializer()
       class Meta:
        model = PersonAccount
        fields = ['id','person','person_category','name','title','full_name','thumbnail','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']

class BankAccountSerializer(serializers.ModelSerializer):
       bank=BankSerializer()
       person=PersonSerializer()
       class Meta:
        model = BankAccount
        fields = ['id','person','bank','name','title','full_name','card_no','account_no','shaba_no','thumbnail','code','balance', 'type','color', 'get_absolute_url','get_edit_url','get_delete_url']
