from django.contrib import admin
from .models import Score,Parent,Group,Course,Word,Teacher,Student,School,Session,CourseClass,EducationalYear,Attendance,Major,ActiveStudent

admin.site.register(Score) 
admin.site.register(Group) 
admin.site.register(Course) 
admin.site.register(Word)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Teacher)
admin.site.register(Session)
admin.site.register(CourseClass)
admin.site.register(ActiveStudent)
admin.site.register(EducationalYear)
admin.site.register(Attendance)
admin.site.register(Major)
admin.site.register(School)