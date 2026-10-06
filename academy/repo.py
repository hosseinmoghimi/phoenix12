from .models import Course,Word
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


     