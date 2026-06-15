from dataclasses import field
from rest_framework import serializers

from archive.models import Folder,File
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Folder
        fields=['id','thumbnail','name','parent_id','get_absolute_url','get_breadcrumb','get_edit_url']


        
class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model=File
        fields=['id','thumbnail','title','get_absolute_url','get_edit_url']