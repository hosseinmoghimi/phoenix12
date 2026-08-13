from accounting.forms import forms,AddInvoiceForm,AddEventForm
 
 
class AddVehicleForm(forms.Form):
    title=forms.CharField( max_length=100, required=True)
    owner_id=forms.IntegerField(required=True)

class AddInvoiceToMaintenanceForm(forms.Form):
    invoice_id=forms.IntegerField(required=True)
    maintenance_id=forms.IntegerField(required=True)
 
class AddInvoiceForm(AddInvoiceForm):
    maintenance_id=forms.IntegerField(required=True)
 
 
class AddMaintenanceForm(AddEventForm):
    hour=forms.IntegerField(  required=False)
    kilometer=forms.IntegerField(  required=False)
    service_man_id=forms.IntegerField(required=True)
    vehicle_id=forms.IntegerField(required=True)
    maintenance_type=forms.CharField(max_length=100, required=True)
    description=forms.CharField(max_length=500, required=False)


class AddOilingMaintenanceForm(AddMaintenanceForm):
    oil_type=forms.CharField(required=False, max_length=50)
    oil_liter=forms.FloatField( required=False)
    fuel_liter=forms.FloatField( required=False)
    replace_oil=forms.BooleanField(required=False)
    over_load_oil=forms.BooleanField(required=False)
   
    
class AddServiceManForm(forms.Form):
    person_account_id=forms.IntegerField(required=True)
     

class AddOilingMaintenanceDetailForm(forms.Form):
    oiling_maintenance_id=forms.IntegerField(required=True)
    count=forms.IntegerField(required=True)
    cost=forms.IntegerField(required=False) 
    filter_action=forms.CharField(required=True, max_length=50)
    filter_type=forms.CharField(required=True, max_length=50)
    description=forms.CharField(required=False, max_length=500)
     
