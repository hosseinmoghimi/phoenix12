from rest_framework import serializers
from .models import Person,MyLink,ClipBoardItem




class PersonSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model=Person
        fields=['id','full_name','image','username','tel','mobile','user_id','get_absolute_url', 'get_edit_url','get_delete_url']
 
 

class PersonFullSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model=Person
        fields=['id','prefix','title','first_name','father_name','last_name','mobile','gender','email','bio','address','type','type2','economic_no','melli_code','birth_date','birth_location','postal_code','tel','image','get_absolute_url', 'get_edit_url','get_delete_url']
 
 
 
 
class MyLinkSerializer(serializers.ModelSerializer):
    person=PersonSerializer()
    class Meta:
        model=MyLink
        fields=['id','person','title','url','priority']


class ClipBoardItemSerializer(serializers.ModelSerializer):
    person=PersonSerializer()
    class Meta:
        model=ClipBoardItem
        fields=['id','person','title','url','priority']

