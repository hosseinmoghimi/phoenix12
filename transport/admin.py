from django.contrib import admin
from .models import Vehicle,MaintenanceInvoice,ServiceMan,Maintenance,OilingMaintenance,Driver,OilingMaintenanceDetail
admin.site.register(Vehicle) 
admin.site.register(MaintenanceInvoice)
admin.site.register(Maintenance)
admin.site.register(OilingMaintenance)
admin.site.register(Driver)
admin.site.register(OilingMaintenanceDetail)
admin.site.register(ServiceMan)