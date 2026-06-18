from django.contrib import admin
from .models import Table,Menu,Order,OrderLog,Barista
 
admin.site.register(Menu)
admin.site.register(Table) 
admin.site.register(Order) 
admin.site.register(OrderLog) 
admin.site.register(Barista) 