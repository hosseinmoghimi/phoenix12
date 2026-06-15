from django.contrib import admin

from archive.models import Folder,File

admin.site.register(Folder)
admin.site.register(File)