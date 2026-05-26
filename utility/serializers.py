from rest_framework import serializers
from .models import  Parameter,Picture 



class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Picture
        fields=['id','name','app_name','image','get_edit_url','get_delete_url']

 
 
class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parameter
        fields=['id','name','app_name','value','get_edit_url','get_delete_url']
