from accounting.forms import AddProductForm,forms,AddInvoiceForm,AddEventForm
from core.forms import EditPageForm

class AddSubProjectForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    parent_id=forms.IntegerField(required=True)
    
class NormalizeProjectForm(forms.Form):
    project_id=forms.IntegerField(required=True)
    
class AddTicketForm(forms.Form):
    title=forms.CharField(max_length=50,required=True)
    parent_id=forms.IntegerField(required=False)
    project_id=forms.IntegerField(required=True)
    person_id=forms.IntegerField(required=True)
    description=forms.CharField(max_length=5000,required=False)
    
class SelectProjectForm(forms.Form):
    project_id=forms.IntegerField(required=True)
 
class AddProjectForm(AddEventForm):
    contractor_id=forms.IntegerField(required=True)
    employer_id=forms.IntegerField(required=True)
    percentage_completed=forms.IntegerField(required=True)
    type=forms.CharField(max_length=50,required=False)
    weight=forms.IntegerField(required=False)
     



class AddEventToProjectForm(AddEventForm):
    project_id=forms.IntegerField(required=True)
    event_id=forms.IntegerField(required=True)
    

class AddInvoiceToProjectForm(forms.Form):
    invoice_id=forms.IntegerField(required=True)
    project_id=forms.IntegerField(required=True)
     
 

class EditProjectForm(EditPageForm):
    project_id=forms.IntegerField(required=True)
    weight=forms.IntegerField(required=False)
    percentage_completed=forms.IntegerField(required=True)
    employer_id=forms.IntegerField(required=False)
    contractor_id=forms.IntegerField(required=False)
    start_datetime=forms.CharField(max_length=20, required=True)
    end_datetime=forms.CharField(max_length=20, required=True)
    archive=forms.BooleanField(required=False)
        
class AddProjectInvoiceForm(AddInvoiceForm):
    project_id=forms.IntegerField(required=True)
 
class AddRemoteClientForm(forms.Form):
    remote_client_id=forms.IntegerField(required=False) 
    project_id=forms.IntegerField(required=True) 
    name=forms.CharField(max_length=50, required=False)
    active_directory=forms.CharField(max_length=100, required=False)
    os=forms.CharField(max_length=50, required=False)
    work_group=forms.CharField(max_length=50, required=False)
    url=forms.CharField(max_length=500, required=False)
    local_ip=forms.CharField(max_length=50, required=False)
    remote_ip=forms.CharField(max_length=50, required=False)
    any_desk_address=forms.CharField(max_length=50, required=False)
    any_desk_password=forms.CharField(max_length=50, required=False)
    dorsan_desk_address=forms.CharField(max_length=50, required=False)
    dorsan_desk_password=forms.CharField(max_length=50, required=False)
    username=forms.CharField(max_length=50, required=False)
    password=forms.CharField(max_length=50, required=False)
    identity=forms.CharField(max_length=50, required=False)
    ssid=forms.CharField(max_length=50, required=False)
    preshared_key=forms.CharField(max_length=50, required=False)
    wireless_band=forms.CharField(max_length=50, required=False)
    wireless_mode=forms.CharField(max_length=50, required=False)
    frequency=forms.CharField(max_length=50, required=False)
    protocol=forms.CharField(max_length=50, required=False)
    channel_width=forms.CharField(max_length=50, required=False)
    adsl_username=forms.CharField(max_length=50, required=False)
    adsl_password=forms.CharField(max_length=50, required=False)
    telephone=forms.CharField(max_length=50, required=False)
    contact=forms.CharField(max_length=50, required=False)
    pattern=forms.CharField(max_length=50, required=False)
    brand_id=forms.IntegerField(required=False)
    product_id=forms.IntegerField(required=False)
    model_name=forms.CharField(max_length=20, required=False)
    id_name=forms.CharField(max_length=20, required=False)
    part_no=forms.CharField(max_length=20, required=False)
    serial_no=forms.CharField(max_length=20, required=False)
    mac_address=forms.CharField(max_length=20, required=False)
    description=forms.CharField(max_length=2000, required=False)

