from .models import Course
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
 