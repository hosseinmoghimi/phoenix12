from django.contrib import admin
from .models import Vehicle,MaintenanceInvoice,ServiceMan,Maintenance
admin.site.register(Vehicle) 
admin.site.register(MaintenanceInvoice)
admin.site.register(Maintenance)
admin.site.register(ServiceMan)