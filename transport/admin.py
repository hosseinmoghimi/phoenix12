from django.contrib import admin
from .models import Product,OilService,FilterService,Vehicle,MaintenanceInvoice
from .models import ServiceMan,Maintenance,WorkShift,Driver,Tavaghof,VehicleStatus
from .models import ProductAnbar,Service
admin.site.register(Vehicle) 
admin.site.register(MaintenanceInvoice)
admin.site.register(Maintenance)
admin.site.register(Driver)
admin.site.register(WorkShift)
admin.site.register(ServiceMan)
admin.site.register(Tavaghof)
admin.site.register(VehicleStatus)
admin.site.register(Product)
admin.site.register(OilService)
admin.site.register(FilterService)
admin.site.register(Service)
admin.site.register(ProductAnbar)