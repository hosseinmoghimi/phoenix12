from django.contrib import admin
from bms.models import Feeder, Log,Relay,Command,Scenario

# Register your models here.
admin.site.register(Feeder)
admin.site.register(Relay)
admin.site.register(Command)
admin.site.register(Log)
admin.site.register(Scenario)