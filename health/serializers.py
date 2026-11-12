from .models import Drug
from rest_framework import serializers

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model=Drug
        fields=['id','title','barcode','color','thumbnail','class_title', 'get_absolute_url', 'get_edit_url','get_delete_url']
 