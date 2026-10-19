from .models import Parent,Group,Course,Word,CourseClass,School,Major,Session,EducationalYear,Attendance,Student,Teacher
from .apps import APP_NAME
from .enums import *
import json
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from accounting.repo import InvoiceLineItemUnitRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import * 


class TeacherRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Teacher.objects.filter(id=0)
        person=PersonRepo(request=request).me
        self.me=Teacher.objects.filter(person_id=person.id).first()
        if person is not None:
            self.objects=Teacher.objects
            if request.user.has_perm(APP_NAME+".view_teacher"):
                self.objects=Teacher.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def teacher(self,*args, **kwargs):
        if "teacher_id" in kwargs and kwargs["teacher_id"] is not None:
            return self.objects.filter(pk=kwargs['teacher_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
         
    def add_teacher(self,*args,**kwargs):
        result,message,teacher=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_teacher"):
            message="دسترسی غیر مجاز"
            return result,message,teacher
        teacher=Teacher()  

        if 'person_id' in kwargs and kwargs['person_id']:
            old=Teacher.objects.filter(person__id=kwargs["person_id"]).first()
            if old is not None:
                message='برای این شخص قبلا دبیر ایجاد شده است.'
                return FAILED,message,None
            teacher.person_id=kwargs["person_id"]
            if teacher.person is not None:
                (result,message,teacher)=teacher.save()
                return result,message,teacher
        from authentication.repo import PersonRepo
        result,message,person=PersonRepo(request=self.request).add_person(**kwargs)
        if result==SUCCEED:     
            teacher.person=person
            (result,message,teacher)=teacher.save()
            return result,message,teacher
        
        return result,message,teacher


class SchoolRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=School.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=School.objects
            if request.user.has_perm(APP_NAME+".view_school"):
                self.objects=School.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def school(self,*args, **kwargs):
        if "school_id" in kwargs and kwargs["school_id"] is not None:
            return self.objects.filter(pk=kwargs['school_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_school(self,*args,**kwargs):
        result,message,school=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_school"):
            message="دسترسی غیر مجاز"
            return result,message,school
        school=School()
        if 'name' in kwargs and kwargs['name']:
            if len(School.objects.filter(name=kwargs["name"]))>0:
                return FAILED,'عنوان تکراری',None
            school.name=kwargs["name"]
        
            
        if 'tel' in kwargs and kwargs['tel']:
            school.tel=kwargs["tel"]
            
        if 'code' in kwargs and kwargs['code']:
            if len(School.objects.filter(code=kwargs['code']))>0:
                return FAILED,'کد تکراری',None
            school.code=kwargs["code"]

            
        

        if 'address' in kwargs and kwargs['address']:
            school.address=kwargs["address"]
        if 'description' in kwargs and kwargs['description']:
            school.description=kwargs["description"]
            
        (result,message,school)=school.save()
        return result,message,school

   
class StudentRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Student.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Student.objects
            if request.user.has_perm(APP_NAME+".view_student"):
                self.objects=Student.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all().order_by('person__first_name').order_by('person__last_name')
        
    def student(self,*args, **kwargs):
        if "student_id" in kwargs and kwargs["student_id"] is not None:
            return self.objects.filter(pk=kwargs['student_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_student(self,*args,**kwargs):
        result,message,student=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_student"):
            message="دسترسی غیر مجاز"
            return result,message,student
        student=Student()  

        if 'color' in kwargs and kwargs['color']:
            student.color=kwargs["color"]



        if 'person_id' in kwargs and kwargs['person_id']:
            old=Student.objects.filter(person__id=kwargs["person_id"]).first()
            if old is not None:
                message='برای این شخص قبلا دانش آموز ایجاد شده است.'
                return FAILED,message,None
            student.person_id=kwargs["person_id"]
            if student.person is not None:
                (result,message,student)=student.save()
                return result,message,student

            
        from authentication.repo import PersonRepo
        result,message,person=PersonRepo(request=self.request).add_person(**kwargs)
        if result==SUCCEED:     
            student.person=person
            (result,message,student)=student.save()
            return result,message,student
         
        return result,message,student
 
  
class CourseRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Course.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Course.objects
            if request.user.has_perm(APP_NAME+".view_course"):
                self.objects=Course.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def course(self,*args, **kwargs):
        if "course_id" in kwargs and kwargs["course_id"] is not None:
            return self.objects.filter(pk=kwargs['course_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_course(self,*args,**kwargs):
        result,message,course=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_course"):
            message="دسترسی غیر مجاز"
            return result,message,course
        course=Course()
        if 'title' in kwargs and kwargs['title']:
            if len(Course.objects.filter(title=kwargs["title"]))>0:
                return FAILED,'عنوان تکراری',None
            course.title=kwargs["title"]
        
            
        if 'level' in kwargs and kwargs['level']:
            course.level=kwargs["level"]
            
        if 'code' in kwargs and kwargs['code']:
            if len(Course.objects.filter(code=kwargs['code']))>0:
                return FAILED,'کد تکراری',None
            course.code=kwargs["code"]

            
        

        if 'nature' in kwargs:
            course.nature=kwargs["nature"]
        (result,message,course)=course.save()
        return result,message,course
  

class MajorRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Major.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Major.objects
            if request.user.has_perm(APP_NAME+".view_major"):
                self.objects=Major.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def major(self,*args, **kwargs):
        if "major_id" in kwargs and kwargs["major_id"] is not None:
            return self.objects.filter(pk=kwargs['major_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_major(self,*args,**kwargs):
        result,message,major=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_major"):
            message="دسترسی غیر مجاز"
            return result,message,major
        major=Major()
        if 'title' in kwargs and kwargs['title']:
            if len(Major.objects.filter(title=kwargs["title"]))>0:
                return FAILED,'عنوان تکراری',None
            major.title=kwargs["title"]
        
            
        if 'level' in kwargs and kwargs['level']:
            major.level=kwargs["level"]
            
        if 'code' in kwargs and kwargs['code']:
            if len(Major.objects.filter(code=kwargs['code']))>0:
                return FAILED,'کد تکراری',None
            major.code=kwargs["code"]

            
        
 
        (result,message,major)=major.save()
        return result,message,major

   
class CourseClassRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=CourseClass.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=CourseClass.objects
            if request.user.has_perm(APP_NAME+".view_course_class"):
                self.objects=CourseClass.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def course_class(self,*args, **kwargs):
        if "course_class_id" in kwargs and kwargs["course_class_id"] is not None:
            return self.objects.filter(pk=kwargs['course_class_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_course_class(self,*args,**kwargs):
        result,message,course_class=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_course_class"):
            message="دسترسی غیر مجاز"
            return result,message,course_class
        course_class=CourseClass()
        if 'title' in kwargs:
            if len(CourseClass.objects.filter(title=kwargs["title"]))>0:
                return FAILED,'عنوان تکراری',None
            course_class.title=kwargs["title"] 

            
        if 'course_id' in kwargs and kwargs['course_id']:
            course_class.course_id=kwargs["course_id"]

        else:
            return FAILED,'واحد درسی را به صورت صحیح وارد کنید.',None
            
        if 'major_id' in kwargs and kwargs['major_id']:
            course_class.major_id=kwargs["major_id"]

        if 'group_id' in kwargs and kwargs['group_id']:
            course_class.group_id=kwargs["group_id"]
        else:
            return FAILED,'رشته تحصیلی را به صورت صحیح وارد کنید.',None

            
        if 'school_id' in kwargs and kwargs['school_id']:
            course_class.school_id=kwargs["school_id"]
        else:
            return FAILED,'آموزشگاه را به صورت صحیح وارد کنید.',None
        if 'level' in kwargs and kwargs['level'] and kwargs['level']>0:
            course_class.level=kwargs["level"]
        else:
            return FAILED,'سطح را به صورت صحیح وارد کنید.',None
            
        if 'educational_year_id' in kwargs and kwargs['educational_year_id']:
            course_class.educational_year_id=kwargs["educational_year_id"]

        else:
            return FAILED,'سال تحصیلی را به صورت صحیح وارد کنید.',None
            
         
        (result,message,course_class)=course_class.save()
        for student in course_class.group.students.all():
            course_class.students.add(student.id)
        return result,message,course_class
 

class WordRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Word.objects.all().order_by('title')
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Word.objects
            if request.user.has_perm(APP_NAME+".view_word"):
                self.objects=Word.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(title__contains=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def word(self,*args, **kwargs):
        if "word_id" in kwargs and kwargs["word_id"] is not None:
            return self.objects.filter(pk=kwargs['word_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_word(self,*args,**kwargs):
        result,message,word=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_word"):
            message="دسترسی غیر مجاز"
            return result,message,word
        word=Word()
        if 'title' in kwargs:
            if len(Word.objects.filter(title=kwargs["title"]))>0:
                return FAILED,'عنوان تکراری',None
            word.title=kwargs["title"] 
        if 'color' in kwargs:
            word.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            word.supplier_id=kwargs["supplier_id"]
        if 'parent_id' in kwargs:
            if kwargs['parent_id'] is not None and kwargs['parent_id']>0:
                word.parent_id=kwargs["parent_id"]

            
        

        if 'nature' in kwargs:
            word.nature=kwargs["nature"]
        (result,message,word)=word.save()
        
        return result,message,word
 
    def delete_all_words(self,*args, **kwargs):
        if self.request.user.has_perm(APP_NAME+".delete_word"):
            Word.objects.all().delete()
            return SUCCEED,"با موفقیت حذف شد."
        return FAILED,"..."
    def import_from_json(self,*args, **kwargs):
        json_file=kwargs['json_file']
        import json
        json_data=json.load(json_file) 
        words=[]

        words = json_data['words']
        add_from_json(words,None,None)
             
              
        return SUCCEED,'با موفقیت بازیابی شد.',words


class SessionRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Session.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Session.objects
            if request.user.has_perm(APP_NAME+".view_session"):
                self.objects=Session.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def session(self,*args, **kwargs):
        if "session_id" in kwargs and kwargs["session_id"] is not None:
            return self.objects.filter(pk=kwargs['session_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_session(self,*args,**kwargs):
        result,message,session=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_session"):
            message="دسترسی غیر مجاز"
            return result,message,session
        session=Session()
        if 'title' in kwargs:
            if len(Session.objects.filter(title=kwargs["title"]))>0:
                return FAILED,'عنوان تکراری',None
            session.title=kwargs["title"] 

        if 'course_class_id' in kwargs and kwargs['course_class_id']:
            session.course_class_id=kwargs["course_class_id"]


        if 'session_no' in kwargs and kwargs['session_no']>0 :
            session.session_no=kwargs["session_no"]
        else:
            return FAILED,'شماره جلسه را صحیح وارد کنید.',None

        if 'class_room' in kwargs and kwargs['class_room']:
            session.class_room=kwargs["class_room"]

 
        if 'start_datetime' in kwargs and kwargs['start_datetime'] is not None and not kwargs['start_datetime']=='':
            year=kwargs['start_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['start_datetime']=PersianCalendar().to_gregorian(kwargs["start_datetime"])
            session.start_datetime=kwargs["start_datetime"]

        if 'end_datetime' in kwargs and kwargs['end_datetime'] is not None and not kwargs['end_datetime']=='':
            year=kwargs['end_datetime'][:2]
            if year=="13" or year=="14":
                kwargs['end_datetime']=PersianCalendar().to_gregorian(kwargs["end_datetime"])
            session.end_datetime=kwargs["end_datetime"]
        a=Session.objects.filter(session_no=session.session_no).filter(course_class_id=session.course_class_id).first()
        if a is not None:
            return FAILED,'شماره جلسه تکراری است',None
        (result,message,session)=session.save()
        return result,message,session
 

class EducationalYearRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=EducationalYear.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=EducationalYear.objects
            if request.user.has_perm(APP_NAME+".view_educational_year"):
                self.objects=EducationalYear.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def educational_year(self,*args, **kwargs):
        if "educational_year_id" in kwargs and kwargs["educational_year_id"] is not None:
            return self.objects.filter(pk=kwargs['educational_year_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_educational_year(self,*args,**kwargs):
        result,message,educational_year=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_educational_year"):
            message="دسترسی غیر مجاز"
            return result,message,educational_year
        educational_year=EducationalYear()
        if 'title' in kwargs:
            if len(EducationalYear.objects.filter(title=kwargs["title"]))>0:
                return FAILED,'عنوان تکراری',None
            educational_year.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                educational_year.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            educational_year.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            educational_year.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            educational_year.priority=kwargs["priority"]
        if 'type' in kwargs:
            educational_year.type=kwargs["type"]

            
        

        if 'nature' in kwargs:
            educational_year.nature=kwargs["nature"]
        (result,message,educational_year)=educational_year.save()
        return result,message,educational_year


class GroupRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Group.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Group.objects
            if request.user.has_perm(APP_NAME+".view_group"):
                self.objects=Group.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs and kwargs['search_for']:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs and kwargs['parent_id']:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  

        if "student_id" in kwargs and kwargs['student_id']:
            student_id=kwargs["student_id"]
            objects=objects.filter(student_id=student_id) 

        if "session_id" in kwargs and kwargs['session_id']:
            session_id=kwargs["session_id"]
            objects=objects.filter(session_id=session_id)  
        return objects.all().order_by('title')
        
    def group(self,*args, **kwargs):
        if "group_id" in kwargs and kwargs["group_id"] is not None:
            return self.objects.filter(pk=kwargs['group_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_group(self,*args,**kwargs):
        result,message,group,groups=FAILED,"",None,[]
        if not self.request.user.has_perm(APP_NAME+".add_group"):
            message="دسترسی غیر مجاز"
            return result,message,group,groups
        olds=Group.objects.filter(title=kwargs['title'])
        if len(olds)>0:
            return FAILED,'عنوان تکراری',None
        group=Group() 

       

        if 'title' in kwargs and kwargs['title'] :
            group.title=kwargs["title"] 
            if kwargs['title'] is None or kwargs['title']=="":
                return FAILED,'عنوان را وارد کنید.',None

        if 'description' in kwargs and kwargs['description']:
            group.description=kwargs["description"] 
 

        if 'code' in kwargs and kwargs['code']:
            group.code=kwargs["code"] 
 
        (result,message,group)=group.save()
         
        return result,message,group
 
  

    def add_student_to_group(self,*args,**kwargs):
        result,message,group,groups=FAILED,"",None,[]
        if not self.request.user.has_perm(APP_NAME+".add_group"):
            message="دسترسی غیر مجاز"
            return result,message,group,groups 
        group_id=kwargs['group_id']
        student_id=kwargs['student_id'] 

        group=Group.objects.filter(pk=group_id).first() 
        student=Student.objects.filter(pk=student_id).first() 

       

        if group is not None:
            if student is not None:
                group.students.add(student.id)
                result=SUCCEED
                message='اضافه شد'
            for course_class in CourseClass.objects.filter(group_id=group.id):
                course_class.students.add(student.id)
         
        return result,message,group
 

class ParentRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Parent.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Parent.objects
            if request.user.has_perm(APP_NAME+".view_group"):
                self.objects=Parent.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs and kwargs['search_for']:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs and kwargs['parent_id']:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  

        if "student_id" in kwargs and kwargs['student_id']:
            student_id=kwargs["student_id"]
            objects=objects.filter(student_id=student_id) 

        if "session_id" in kwargs and kwargs['session_id']:
            session_id=kwargs["session_id"]
            objects=objects.filter(session_id=session_id)  
        return objects.all().order_by('person__last_name')
        
    def parent(self,*args, **kwargs):
        if "parent_id" in kwargs and kwargs["parent_id"] is not None:
            return self.objects.filter(pk=kwargs['parent_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_parent(self,*args,**kwargs):
        result,message,parent,parents=FAILED,"",None,[]
        if not self.request.user.has_perm(APP_NAME+".add_parent"):
            message="دسترسی غیر مجاز"
            return result,message,parent,parents
         
        from authentication.repo import PersonRepo
        result,message,person=PersonRepo(request=self.request).add_person(*args,**kwargs)
        parent=Parent(person=person) 
        if person is None:
            return FAILED,message,None
        (result,message,parent)=parent.save()
         
        return result,message,parent
 
  

    def set_students_for_parent(self,*args,**kwargs):
        result,message,parent,parents=FAILED,"",None,[]
        if not self.request.user.has_perm(APP_NAME+".add_parent"):
            message="دسترسی غیر مجاز"
            return result,message,parent,parents 
        parent_id=kwargs['parent_id']
        students_ids=kwargs['students_ids'] 

        parent=Parent.objects.filter(pk=parent_id).first() 
        students=Student.objects.filter(pk__in=students_ids)
        if students is None:
        
            result=FAILED
            message='دانش آموزی انتخاب نشده است'
            return FAILED,message,None

        # parent.students.clear()
        if parent is not None:
            for student in students:
                parent.students.add(student.id)
                result=SUCCEED
                message='اضافه شد'
             
        students=parent.students.all() 
        return result,message,students
  

class AttendanceRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Attendance.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Attendance.objects
            if request.user.has_perm(APP_NAME+".view_attendance"):
                self.objects=Attendance.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs and kwargs['search_for']:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs and kwargs['parent_id']:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  

        if "student_id" in kwargs and kwargs['student_id']:
            student_id=kwargs["student_id"]
            objects=objects.filter(student_id=student_id) 

        if "student_id__in" in kwargs and kwargs['student_id__in']:
            student_id__in=kwargs["student_id__in"]
            objects=objects.filter(student_id__in=student_id__in) 
        if "session_id" in kwargs and kwargs['session_id']:
            session_id=kwargs["session_id"]
            objects=objects.filter(session_id=session_id)  
        return objects.all().order_by('student__person__last_name')
        
    def attendance(self,*args, **kwargs):
        if "attendance_id" in kwargs and kwargs["attendance_id"] is not None:
            return self.objects.filter(pk=kwargs['attendance_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_attendance(self,*args,**kwargs):
        result,message,attendance,attendances=FAILED,"",None,[]
        if not self.request.user.has_perm(APP_NAME+".add_attendance"):
            message="دسترسی غیر مجاز"
            return result,message,attendance,attendances
        attendance=Attendance() 

        if 'student_id' in kwargs and kwargs['student_id']:
            attendance.student_id=kwargs["student_id"] 


        if 'session_id' in kwargs and kwargs['session_id']:
            attendance.session_id=kwargs["session_id"] 


        if 'status' in kwargs and kwargs['status']:
            attendance.status=kwargs["status"] 


        if 'description' in kwargs and kwargs['description']:
            attendance.description=kwargs["description"] 

        teacher=TeacherRepo(request=self.request).me

        if teacher is not None:
            attendance.teacher_id=teacher.id

        Attendance.objects.filter(session_id=attendance.session_id).filter(student_id=attendance.student_id).delete()
        (result,message,attendance)=attendance.save()
        attendances=AttendanceRepo(request=self.request).list(session_id=attendance.session.id)
        return result,message,attendance,attendances
 
  
def add_from_json(words=[],parent_id=None,new_parent_id=None): 
    if len(words)<1:
        return
    for word in words: 
        word['id']=int(word['id'])
        if word['parent_id'] is not None:
            word['parent_id']=int(word['parent_id'])
        
        if word['parent_id']==parent_id:
            new_word=Word()
            new_word.parent_id=new_parent_id
            new_word.title=word['title'] 
            new_word.app_name=APP_NAME
            new_word.class_name='word'
            new_word.thumbnail_origin=word['thumbnail_origin']
            new_word.save()
            # words.remove(word)
            
            add_from_json(words=words,parent_id=int(word['id']),new_parent_id=new_word.id)


     