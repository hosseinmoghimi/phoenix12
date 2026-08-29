from accounting.forms import forms,AddInvoiceForm,AddEventForm
 
 
class AddVehicleForm(forms.Form):
    owner_id=forms.IntegerField(required=False)
    title=forms.CharField( max_length=100, required=False)
    vehicle_color=forms.CharField( max_length=100, required=False)
    vehicle_code=forms.CharField( max_length=100, required=False)
    vehicle_type=forms.CharField( max_length=100, required=False)
    model_name=forms.CharField( max_length=100, required=False)
    brand_name=forms.CharField( max_length=100, required=False)
    year=forms.CharField( max_length=100, required=False)
    plaque=forms.CharField( max_length=100, required=False)
    kilometer=forms.IntegerField(required=False)
    driver_id=forms.IntegerField(required=False)
    price=forms.IntegerField(required=False)


class AddInvoiceToMaintenanceForm(forms.Form):
    invoice_id=forms.IntegerField(required=True)
    maintenance_id=forms.IntegerField(required=True)

 
class AddInvoiceForm(AddInvoiceForm):
    maintenance_id=forms.IntegerField(required=True)
 
 
class AddMaintenanceForm(AddEventForm):
    hour=forms.IntegerField(  required=False)
    kilometer=forms.IntegerField(  required=False)
    service_man_id=forms.IntegerField(required=True)
    driver_id=forms.IntegerField(required=False)
    vehicle_id=forms.IntegerField(required=True)
    maintenance_type=forms.CharField(max_length=100, required=True)
    description=forms.CharField(max_length=500, required=False)


class AddKarkerdForm(AddEventForm): 
    driver_id=forms.IntegerField(required=True)
    vehicle_id=forms.IntegerField(required=True)
    description=forms.CharField(max_length=500, required=False)
    start_datetime=forms.CharField(max_length=50, required=False)
    end_datetime=forms.CharField(max_length=50, required=False)
    project_name=forms.CharField(max_length=50, required=False)
    area_name=forms.CharField(max_length=50, required=False)

    start_hour=forms.FloatField(required=False)
    end_hour=forms.FloatField(required=False)
    
    start_kilometer=forms.IntegerField( required=False)
    end_kilometer=forms.IntegerField( required=False)

    load=forms.CharField( max_length=50,required=False)
    count=forms.IntegerField( required=False)

    
class AddOilingMaintenanceForm(AddMaintenanceForm):
    oil_type=forms.CharField(required=False, max_length=50)
    oil_liter=forms.FloatField( required=False)
    fuel_liter=forms.FloatField( required=False)
    replace_oil=forms.BooleanField(required=False)
    over_load_oil=forms.BooleanField(required=False)
   
    
class AddServiceManForm(forms.Form):
    person_account_id=forms.IntegerField(required=True)

     
class VehicleStatusesExcelForm(forms.Form):
    vehicle_id=forms.IntegerField(required=False) 

class OilingMaintenanceDetailsExcelForm(forms.Form):
    oiling_maintenance_id=forms.IntegerField(required=False) 

class ImportVehicleStatusFromExcelForm(forms.Form):
    count=forms.IntegerField(required=False) 

class AddOilingMaintenanceDetailForm(forms.Form):
    oiling_maintenance_id=forms.IntegerField(required=True)
    count=forms.IntegerField(required=True)
    cost=forms.IntegerField(required=False) 
    filter_action=forms.CharField(required=True, max_length=50)
    filter_type=forms.CharField(required=True, max_length=50)
    description=forms.CharField(required=False, max_length=500)
     


class AddWorkShiftForm(forms.Form):
    vehicle_code=forms.CharField(required=True, max_length=50) 
    driver_id=forms.IntegerField(required=False)
    location=forms.CharField(required=False, max_length=50) 
    


    shift=forms.CharField(required=False, max_length=50) 
    shift_date=forms.CharField(required=False, max_length=50) 
    start_hour=forms.IntegerField(required=False) 
    end_hour=forms.IntegerField(required=False)  


    vehicle_start_hour=forms.FloatField(required=False) 
    vehicle_end_hour=forms.FloatField(required=False)

    
    bar=forms.CharField(required=True, max_length=50) 
    service_count=forms.IntegerField(required=False)

    description=forms.CharField(required=False, max_length=500)

    gasoil_liter=forms.IntegerField(required=False)


    oils=forms.CharField(required=False, max_length=5000)
    filters=forms.CharField(required=False, max_length=5000)
    tavaghofs=forms.CharField(required=False, max_length=5000)
    products=forms.CharField(required=False, max_length=5000)

 
     
    
class GetReportForm(forms.Form):
    vehicle_code=forms.CharField(required=False, max_length=50) 
    driver_id=forms.IntegerField(required=False)
    location=forms.CharField(required=False, max_length=50) 
    shift_date=forms.CharField(required=False, max_length=50) 
    from_shift_date=forms.CharField(required=False, max_length=50) 
    to_shift_date=forms.CharField(required=False, max_length=50) 
    shift=forms.CharField(required=False, max_length=50) 
     
class VehiclesExcelForm(forms.Form):
    pass
     
    
class ImportVehicleFromExcelForm(forms.Form):
    count=forms.IntegerField( required=False)

class AddServiceForm(forms.Form):
    grease=forms.IntegerField( required=False)
    shift_date=forms.CharField(required=False, max_length=50) 
    shift=forms.CharField(required=False, max_length=50) 
    vehicle_id=forms.IntegerField(required=False)
    service_man_id=forms.IntegerField(required=False)
    driver_id=forms.IntegerField(required=False)
    oil_type=forms.CharField(required=False, max_length=50) 
    oil_liter=forms.IntegerField(required=False)
    vehicle_hour=forms.FloatField(required=False)
    filter_type=forms.CharField(required=False, max_length=50) 
    filter_action=forms.CharField(required=False, max_length=50) 
    description=forms.CharField(required=False, max_length=500) 
                
        