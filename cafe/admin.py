from django.contrib import admin
from .models import Table,Menu,TableCustomer,MenuItem
 
admin.site.register(TableCustomer)
admin.site.register(Menu)
admin.site.register(Table)
admin.site.register(MenuItem)