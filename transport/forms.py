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
    kilometer=forms.IntegerField(  required=False)
    service_man_id=forms.IntegerField(required=True)
    vehicle_id=forms.IntegerField(required=True)
    maintenance_type=forms.CharField(max_length=100, required=True)
    description=forms.CharField(max_length=500, required=False)
    

    
class AddServiceManForm(forms.Form):
    person_account_id=forms.IntegerField(required=True)
     
