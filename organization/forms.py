from accounting.forms import AddProductForm,forms
 
class AddOrganizationalUnitForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    person_account_id=forms.IntegerField(required=True)
    parent_id=forms.IntegerField(required=False)
    
 
class AddEmployeeForm(forms.Form):
    job_title=forms.CharField(max_length=50,required=True)
    organizational_unit_id=forms.IntegerField(required=True)
    person_account_id=forms.IntegerField(required=True)
    
 
class SelectOrganizationalUnitForm(forms.Form):
    organizational_unit_id=forms.IntegerField(required=True)
    
 
class SelectEmployeeForm(forms.Form):
    employee_id=forms.IntegerField(required=True)
    
 