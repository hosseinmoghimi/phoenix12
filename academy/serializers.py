from rest_framework import serializers
from authentication.serializers import PersonSerializer
from .models import Course,Word,CourseClass,Teacher,Student,Attendance,EducationalYear,Session
 
  
class EducationalYearSerializer(serializers.ModelSerializer): 
    class Meta:
        model=EducationalYear
        fields=['id','name', 'get_absolute_url', 'get_edit_url','get_delete_url']
       
class CourseSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Course
        fields=['id','title', 'get_absolute_url', 'get_edit_url','get_delete_url']
  

  
class StudentSerializer(serializers.ModelSerializer): 
    person=PersonSerializer()
    class Meta:
        model=Student
        fields=['id','full_name','person', 'get_absolute_url', 'get_edit_url','get_delete_url']
    
    
class TeacherSerializer(serializers.ModelSerializer): 
    person=PersonSerializer()
    class Meta:
        model=Teacher
        fields=['id','full_name','person', 'get_absolute_url', 'get_edit_url','get_delete_url']


class CourseClassSerializer(serializers.ModelSerializer): 
    educational_year=EducationalYearSerializer()
    course=CourseSerializer()
    teachers=TeacherSerializer(many=True)
    class Meta:
        model=CourseClass
        fields=['id','title','teachers','course','educational_year', 'get_absolute_url', 'get_edit_url','get_delete_url']

           
class SessionSerializer(serializers.ModelSerializer): 
    course_class=CourseClassSerializer()
    class Meta:
        model=Session
        fields=['id','course_class','title', 'get_absolute_url', 'get_edit_url','get_delete_url']
    
     
class WordSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Word
        fields=['id','title','thumbnail', 'get_absolute_url', 'get_edit_url','get_delete_url']
  