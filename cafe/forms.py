from accounting.forms import AddProductForm,forms

class AddTableForm(forms.Form):
    table_no=forms.IntegerField(required=True)
    title=forms.CharField(max_length=50,required=True)
    code=forms.CharField(max_length=500,required=True)
    supplier_id=forms.IntegerField(required=True)


class AddMenuForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    supplier_id=forms.IntegerField(required=True)
     

class CheckoutCartForm(forms.Form):
    cart_items=forms.CharField(max_length=500, required=True)
    table_id=forms.IntegerField(required=True)
    customer_id=forms.IntegerField( required=False)
    description=forms.CharField( max_length=200, required=False)

    
class LoginTableForm(forms.Form):
    table_id=forms.IntegerField(required=True)