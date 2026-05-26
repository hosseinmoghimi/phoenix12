from django.contrib import admin
from .models import Shop,Customer,Supplier,Shipper,CartItem,ShopPackage

admin.site.register(CartItem)
admin.site.register(Customer)
admin.site.register(Shop)
admin.site.register(Supplier)
admin.site.register(Shipper)
admin.site.register(ShopPackage)