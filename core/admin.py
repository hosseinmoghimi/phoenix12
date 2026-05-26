from django.contrib import admin

from .models import Page,EventCategory,Event 
admin.site.register(Page)
admin.site.register(EventCategory)
admin.site.register(Event)