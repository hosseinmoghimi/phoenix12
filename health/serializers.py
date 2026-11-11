from .models import Drug
from rest_framework import serializers

class DrugSerializer(serializers.Serializer):
    class Meta:
        model=Drug
        fields=['id','title','color', 'get_absolute_url', 'get_edit_url','get_delete_url']
 