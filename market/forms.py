from django import forms


class AddShopToMenuForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    supplier_id=forms.IntegerField(required=True)

    
class AddShopForm(forms.Form): 
    unit_name=forms.CharField(max_length=100, required=True)
    unit_price=forms.IntegerField(required=True)
    available=forms.IntegerField(required=True)
    group_id=forms.IntegerField(required=True)
    region_id=forms.IntegerField(required=True)
    product_id=forms.IntegerField(required=True)
    supplier_id=forms.IntegerField(required=False)
    coef=forms.IntegerField(required=False)
    discount_percentage=forms.IntegerField(required=False)
    menu_id=forms.IntegerField(required=False)
    menu_title=forms.CharField(max_length=100, required=False)
    start_date=forms.CharField(max_length=100, required=False)
    end_date=forms.CharField(max_length=100, required=False)
     
class ImportShopFromExcelForm(forms.Form): 
    count=forms.IntegerField(required=True)

     
class AddShopsForm(forms.Form): 
    group_id=forms.IntegerField(required=True)
    shops=forms.CharField(max_length=5000, required=True)
    region_id=forms.IntegerField(required=True)
    supplier_id=forms.IntegerField(required=False)
    start_date=forms.CharField(max_length=100, required=False)
    end_date=forms.CharField(max_length=100, required=False)
    
class SearchForm(forms.Form): 
    search_for=forms.CharField(max_length=100, required=True)

    
class SelectCategoryForm(forms.Form): 
    category_id=forms.IntegerField(required=True)
    

class ExportShopsToExcelForm(forms.Form): 
    supplier_id=forms.IntegerField(required=True)
    region_id=forms.IntegerField(required=True)
    group_id=forms.IntegerField(required=True)
    
class CheckoutCartForm(forms.Form):
    address=forms.CharField(max_length=100, required=True)
    postal_code=forms.CharField(max_length=100, required=True)
    cart_items=forms.CharField(max_length=1000, required=True)
    address=forms.CharField(max_length=200, required=False)
    postal_code=forms.CharField(max_length=50, required=False)
    customer_id=forms.IntegerField(required=True)
    description=forms.CharField(max_length=500, required=False)
    
class AddCartItemForm(forms.Form):
    unit_name=forms.CharField(max_length=100, required=False)
    shop_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=False)
    
class ChangeCartItemForm(forms.Form):
    unit_name=forms.CharField(max_length=100, required=False)
    shop_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=False)

class AddMarketPersonForm(forms.Form): 
    groups_ids=forms.CharField( max_length=100, required=False)
    person_account_id=forms.IntegerField(required=True)
    region_id=forms.IntegerField(required=True)
   
class AddCartLineForm(forms.Form):
    shop_id=forms.IntegerField(required=True)
   


class AddCustomerForm(AddMarketPersonForm):
    person_account_categories=forms.CharField(max_length=200, required=False)

class AddShipperForm(AddMarketPersonForm):
    person_account_categories=forms.CharField(max_length=200, required=False)

 
class AddSupplierForm(AddMarketPersonForm):
    person_account_categories=forms.CharField(max_length=200, required=False)

class AddSupplierByPersonForm(forms.Form): 
    person_id=forms.IntegerField(required=True)  
     

