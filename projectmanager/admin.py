from django.contrib import admin
from .models import Ticket,Project,RemoteClient,Issue

admin.site.register(RemoteClient)
admin.site.register(Project) 
admin.site.register(Issue)
admin.site.register(Ticket)
# Register your models here.
