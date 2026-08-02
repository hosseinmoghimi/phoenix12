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
     
class AddOilingForm(AddMaintenanceForm):
    kilometer=forms.IntegerField(  required=False)
    service_man_id=forms.IntegerField(required=True)
    vehicle_id=forms.IntegerField(required=True)
    maintenance_type=forms.CharField(max_length=100, required=True)
    description=forms.CharField(max_length=500, required=False)
    oil_type=forms.CharField(required=False, max_length=50)
    oil_liter=forms.FloatField( required=False)
    oil_filter=forms.BooleanField(required=False)
    gasoil_filter=forms.BooleanField(required=False)
    Hydrolic_filter=forms.BooleanField(required=False)
    nano_filter=forms.BooleanField(required=False)
    abgir_filter=forms.BooleanField(required=False)
    tank_filter=forms.BooleanField(required=False)
    bokharkesh_filter=forms.BooleanField(required=False)
    lajangir_filter=forms.BooleanField(required=False)

    
class AddServiceManForm(forms.Form):
    person_account_id=forms.IntegerField(required=True)
     
