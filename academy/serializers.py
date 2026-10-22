from rest_framework import serializers
from authentication.serializers import Person
from .models import Parent,Group,Course,Word,CourseClass,Teacher,Student,Major,Attendance,EducationalYear,Session,School
 
  
class EducationalYearSerializer(serializers.ModelSerializer): 
    class Meta:
        model=EducationalYear
        fields=['id','name', 'get_absolute_url', 'get_edit_url','get_delete_url']
  
class GroupSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Group
        fields=['id','title','code','student_count', 'get_absolute_url', 'get_edit_url','get_delete_url']

class SchoolSerializer(serializers.ModelSerializer): 
    class Meta:
        model=School
        fields=['id','name','code', 'get_absolute_url', 'get_edit_url','get_delete_url']


class MajorSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Major
        fields=['id','title', 'get_absolute_url', 'get_edit_url','get_delete_url']


class CourseSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Course
        fields=['id','thumbnail','class_count','title','code', 'get_absolute_url', 'get_edit_url','get_delete_url']
 
class PersonSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Person
        fields=['id','full_name','first_name','last_name','melli_code','image','username','tel','mobile','user_id','get_absolute_url', 'get_edit_url','get_delete_url']
 
  
class StudentSerializer(serializers.ModelSerializer): 
    person=PersonSerializer()
    class Meta:
        model=Student
        fields=['id','full_name','first_name','last_name','melli_code','person', 'get_absolute_url', 'get_edit_url','get_delete_url']
    
    
class TeacherSerializer(serializers.ModelSerializer): 
    person=PersonSerializer()
    class Meta:
        model=Teacher
        fields=['id','personneli_code', 'full_name','person', 'get_absolute_url', 'get_edit_url','get_delete_url']


class CourseClassSerializer(serializers.ModelSerializer): 
    educational_year=EducationalYearSerializer()
    group=GroupSerializer()
    major=MajorSerializer()
    school=SchoolSerializer()
    course=CourseSerializer()
    teachers=TeacherSerializer(many=True)
    class Meta:
        model=CourseClass
        fields=['id','group','title','school','student_count','major','level','teachers','course','educational_year', 'get_absolute_url', 'get_edit_url','get_delete_url']

           
class SessionSerializer(serializers.ModelSerializer): 
    course_class=CourseClassSerializer()
    class Meta:
        model=Session
        fields=['id','thumbnail','course_class','session_no','class_room','persian_event_datetime','persian_start_datetime','persian_end_datetime','title', 'get_absolute_url', 'get_edit_url','get_delete_url']
    
     
class WordSerializer(serializers.ModelSerializer): 
    class Meta:
        model=Word
        fields=['id','title','thumbnail', 'get_absolute_url', 'get_edit_url','get_delete_url']

  
class AttendanceSerializer(serializers.ModelSerializer): 
    student=StudentSerializer()
    session=SessionSerializer()
    class Meta:
        model=Attendance
        fields=['id','student','status','session','get_edit_url','get_delete_url']


class ParentSerializer(serializers.ModelSerializer): 
    person=PersonSerializer()
    students=StudentSerializer(many=True)
    class Meta:
        model=Parent
        fields=['id','person','students','get_absolute_url', 'get_edit_url','get_delete_url']
    
  