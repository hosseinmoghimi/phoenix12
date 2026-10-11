from .models import Course,Word,CourseClass,Session,EducationalYear,Attendance,Student,Teacher
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
        if 'title' in kwargs:
            if len(Teacher.objects.filter(title=kwargs["title"]))>0:
                return FAILED,'عنوان تکراری',None
            teacher.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                teacher.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            teacher.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            teacher.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            teacher.priority=kwargs["priority"]
        if 'type' in kwargs:
            teacher.type=kwargs["type"]

            
        

        if 'nature' in kwargs:
            teacher.nature=kwargs["nature"]
        (result,message,teacher)=teacher.save()
        return result,message,teacher

 
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
        return objects.all()
        
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
        if 'title' in kwargs:
            if len(Student.objects.filter(title=kwargs["title"]))>0:
                return FAILED,'عنوان تکراری',None
            student.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                student.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            student.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            student.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            student.priority=kwargs["priority"]
        if 'type' in kwargs:
            student.type=kwargs["type"]

            
        

        if 'nature' in kwargs:
            student.nature=kwargs["nature"]
        (result,message,student)=student.save()
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
        if 'title' in kwargs:
            if len(Course.objects.filter(title=kwargs["title"]))>0:
                return FAILED,'عنوان تکراری',None
            course.title=kwargs["title"]
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                course.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            course.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            course.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            course.priority=kwargs["priority"]
        if 'type' in kwargs:
            course.type=kwargs["type"]

            
        

        if 'nature' in kwargs:
            course.nature=kwargs["nature"]
        (result,message,course)=course.save()
        return result,message,course
  
 
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
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                course_class.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            course_class.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            course_class.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            course_class.priority=kwargs["priority"]
        if 'type' in kwargs:
            course_class.type=kwargs["type"]

            
        

        if 'nature' in kwargs:
            course_class.nature=kwargs["nature"]
        (result,message,course_class)=course_class.save()
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
        if 'parent_id' in kwargs:
            if kwargs["parent_id"]>0:
                session.parent_id=kwargs["parent_id"]
        if 'color' in kwargs:
            session.color=kwargs["color"]
        if 'supplier_id' in kwargs:
            session.supplier_id=kwargs["supplier_id"]
        if 'priority' in kwargs:
            session.priority=kwargs["priority"]
        if 'type' in kwargs:
            session.type=kwargs["type"]

            
        

        if 'nature' in kwargs:
            session.nature=kwargs["nature"]
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


     