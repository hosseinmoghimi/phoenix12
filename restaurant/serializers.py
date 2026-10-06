from rest_framework import serializers
from .models import Food
 
 
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Food 
        fields=['id','code','title','get_absolute_url', 'get_edit_url','get_delete_url']
  
 