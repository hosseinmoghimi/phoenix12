from django.contrib import admin
from .models import Vehicle,MaintenanceInvoice,ServiceMan,Maintenance,WorkShift,OilingMaintenance,Driver,OilingMaintenanceDetail,Karkerd,Tavaghof,VehicleStatus
admin.site.register(Vehicle) 
admin.site.register(MaintenanceInvoice)
admin.site.register(Maintenance)
admin.site.register(OilingMaintenance)
admin.site.register(Driver)
admin.site.register(WorkShift)
admin.site.register(OilingMaintenanceDetail)
admin.site.register(ServiceMan)
admin.site.register(Karkerd)
admin.site.register(Tavaghof)
admin.site.register(VehicleStatus)