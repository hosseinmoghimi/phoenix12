from django.contrib import admin
from .models import Course,Word,Teacher,Student,Session,CourseClass,EducationalYear,Attendance

admin.site.register(Course) 
admin.site.register(Word)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Session)
admin.site.register(CourseClass)
admin.site.register(EducationalYear)
admin.site.register(Attendance)