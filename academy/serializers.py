from rest_framework import serializers
from .models import Course,Word
 
  
class CourseSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Course
        fields=['id','title', 'get_absolute_url', 'get_edit_url','get_delete_url']
  

   
  
  
class WordSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Word
        fields=['id','title','thumbnail', 'get_absolute_url', 'get_edit_url','get_delete_url']
  