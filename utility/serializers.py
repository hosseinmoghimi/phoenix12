from rest_framework import serializers
from .models import  Parameter,Picture,Region,City,State



class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model=State
        fields=['id','name','get_absolute_url']

class CitySerializer(serializers.ModelSerializer):
    state=StateSerializer()
    class Meta:
        model=City
        fields=['id','name','state','get_absolute_url']

class RegionSerializer(serializers.ModelSerializer):
    city=CitySerializer()
    class Meta:
        model=Region
        fields=['id','name','city','get_absolute_url']

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Picture
        fields=['id','name','app_name','image','get_edit_url','get_delete_url']

 
 
class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parameter
        fields=['id','name','app_name','value','get_edit_url','get_delete_url']
