from accounting.forms import AddProductForm,forms

class AddWareHouseForm(forms.Form):
    name=forms.CharField(max_length=50,required=True)
    person_account_id=forms.IntegerField(required=True) 

class AddMaterialRequestForm(forms.Form):
    warehouse_id=forms.IntegerField(required=False)
    product_id=forms.IntegerField(required=True)
    row=forms.IntegerField(required=False)
    invoice_id=forms.IntegerField(required=False)
    organizational_unit_id=forms.IntegerField(required=False)
    quantity=forms.FloatField(required=True)
    unit_price=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50,required=False)
    type=forms.CharField(max_length=50,required=False)
    default_price=forms.BooleanField(required=False)
    save=forms.BooleanField(required=False)
    direction=forms.CharField(max_length=50,required=False)
    description=forms.CharField(max_length=500,required=False)
    coef=forms.IntegerField(required=False)
    unit_name=forms.CharField(max_length=100, required=True)

class NormalizeProductInWareHouseForm(forms.Form):
    warehouse_id=forms.IntegerField(required=True) 
    product_id=forms.IntegerField(required=False) 

class AddInvoiceWareHouseSheetsForm(forms.Form):
    invoice_id=forms.IntegerField(required=True) 
    organizational_unit_id=forms.IntegerField(required=False) 
    warehouse_id=forms.IntegerField(required=True) 
    shelf=forms.CharField(required=False,max_length=50)
    row=forms.CharField(required=False,max_length=50)
    col=forms.CharField(required=False,max_length=50)
    direction=forms.CharField(required=True,max_length=50)
    description=forms.CharField(required=False,max_length=500)
     

class AddWareHouseSheetForm(forms.Form):
    invoice_line_id=forms.IntegerField(required=True) 
    organizational_unit_id=forms.IntegerField(required=False) 
    warehouse_id=forms.IntegerField(required=True) 
    shelf=forms.CharField(required=False,max_length=50)
    row=forms.CharField(required=False,max_length=50)
    col=forms.CharField(required=False,max_length=50)
    direction=forms.CharField(required=True,max_length=50)
    status=forms.CharField(required=False,max_length=50)
    type=forms.CharField(required=False,max_length=50)
    description=forms.CharField(required=False,max_length=500)
     
class SelectWareHouseForm(forms.Form):
    warehouse_id=forms.IntegerField(required=True) 
    
    
class ProductInWareHouseForm(forms.Form):
    product_id=forms.IntegerField(required=True) 
    warehouse_id=forms.IntegerField(required=False) 


class AddWareHouseSheetSignatureForm(forms.Form):
    warehouse_sheet_id=forms.IntegerField(required=True) 
    status=forms.CharField(required=True,max_length=50)
    description=forms.CharField(required=False,max_length=500)

class AddWareHouseSheetLabelForm(forms.Form):
    warehouse_sheet_id=forms.IntegerField(required=True) 
    serial_no=forms.CharField(required=True,max_length=50)
    description=forms.CharField(required=False,max_length=500)