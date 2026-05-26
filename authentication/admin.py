from django.contrib import admin
 
from .models import Person,ClipBoardItem,MyLink
admin.site.register(ClipBoardItem)
admin.site.register(MyLink)

admin.site.register(Person)