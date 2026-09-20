from .models import Food 
from .apps import APP_NAME
from .enums import *
import json
from log.repo import LogRepo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo 
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *  


class FoodRepo():
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        self.objects=Food.objects.filter(id=0)
        person=PersonRepo(request=request).me

        if person is not None:
            self.objects=Food.objects
            if request.user.has_perm(APP_NAME+".view_food"):
                self.objects=Food.objects
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        return objects.all()
        
    def food(self,*args, **kwargs):
        if "food_id" in kwargs and kwargs["food_id"] is not None:
            return self.objects.filter(pk=kwargs['food_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_food(self,*args,**kwargs):
        result,message,food=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_food"):
            message="دسترسی غیر مجاز"
            return result,message,food
        
        if len(Food.objects.filter(title=kwargs['title']))>0:
            return FAILED,'عنوان تکراری برای غذای جدید',None
        
        if len(Food.objects.filter(code=kwargs['code']))>0:
            return FAILED,'کد تکراری برای غذای جدید',None
        
        food=Food()
        if 'title' in kwargs and kwargs['title']:
            food.title=kwargs["title"]
         
        if 'code' in kwargs and kwargs['code']:
            food.code=kwargs["code"]
            
        (result,message,food)=food.save()
        return result,message,food
 
    def delete_all_foods(self,*args,**kwargs):
        result,message=FAILED,""
        if not self.request.user.has_perm(APP_NAME+".delete_food"):
            message="دسترسی غیر مجاز"
            return result,message
        Food.objects.all().delete()
        
        (result,message)=(SUCCEED,'همه غذا ها حذف شد.')
        return result,message


  
    def initial_default_foods(self,*args,**kwargs):
        result,message,foods=FAILED,"",[]
        if not self.request.user.has_perm(APP_NAME+".add_food"):
            message="دسترسی غیر مجاز"
            return result,message,foods
        from .defaults import initial_foods
        foods=[]
        counter=0
        for food1 in initial_foods:
            (result,message,food)=self.add_food(**food1)
            if result==SUCCEED:
                foods.append(food)
                counter+=1
        (result,message,foods)=(SUCCEED,'همه غذا های پیش فرض اضافه شدند.'+'<br>'+f'{counter} عنوان جدید',foods)
        return result,message,foods
   