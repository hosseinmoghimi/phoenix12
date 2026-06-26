from rest_framework import serializers
from .models import Course 
 
  
class CourseSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Course
        fields=['id','title', 'get_absolute_url', 'get_edit_url','get_delete_url']
  