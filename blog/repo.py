from .models import Blog,HomeSlider,AboutUs,ContactUs
from .apps import APP_NAME
from .enums import *
from log.repo import LogRepo
from core.repo import Repo 
from django.db.models import Q
from django.shortcuts import reverse
from authentication.repo import PersonRepo
from utility.num import filter_number
from utility.calendar import PersianCalendar
from utility.constants import FAILED,SUCCEED
from utility.log import leolog
from .enums import *

class AboutUsRepo(Repo):

    def __init__(self,request,*args, **kwargs):
        super(AboutUsRepo,self).__init__(request,app_name=APP_NAME,*args, **kwargs)
        self.objects=AboutUs.objects
    def get(self):
        return AboutUs.objects.filter(pk=1).first()
    
    def set(self,new_value):
        if self.request.user.has_perm(APP_NAME+".change_aboutus"):
            aa=AboutUs.objects.first()
            if aa is None:
                aa=AboutUs()
            aa.id=1
            aa.about=new_value
            aa.save()



class BlogRepo(Repo):

    def __init__(self,request,*args, **kwargs):
        super(BlogRepo,self).__init__(request,app_name=APP_NAME,*args, **kwargs)
        self.me=None
        self.my_accounts=[]
        self.request=request
        self.objects=Blog.objects.filter(id=0)
        self.objects=Blog.objects
                
    def list(self,*args, **kwargs):
        objects=self.objects
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(name__contains=search_for) | Q(code=search_for)  )
        if "parent_id" in kwargs:
            parent_id=kwargs["parent_id"]
            objects=objects.filter(parent_id=parent_id)  
        if "for_home" in kwargs:
            for_home=kwargs["for_home"]
            from django.utils import timezone
            now=timezone.now()
            objects=objects.filter(for_home=for_home).filter(start_date__lte=now).filter(end_date__gte=now)  
        return objects.all()
        
    def blog(self,*args, **kwargs):
        if "blog_id" in kwargs and kwargs["blog_id"] is not None:
            return self.objects.filter(pk=kwargs['blog_id']).first()  
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        
        
    def add_blog(self,*args,**kwargs):
        result,message,blog=FAILED,"",None
        if len(Blog.objects.filter(title=kwargs["title"]))>0:
            message='عنوان تکراری برای بلاگ جدید'
            return FAILED,message,None
        
            return FAILED,message,None
        if not self.request.user.has_perm(APP_NAME+".add_blog"):
            message="دسترسی غیر مجاز"
            return result,message,blog

        blog=Blog() 
        if 'title' in kwargs:
            blog.title=kwargs["title"]
        
        (result,message,blog)=blog.save()
        return result,message,blog
    



class HomeSliderRepo(Repo):
    def __init__(self,request,*args, **kwargs):
        super(HomeSliderRepo,self).__init__(request,app_name=APP_NAME,*args, **kwargs)
 
        self.objects=HomeSlider.objects.filter(archive=False)
    def list(self,*args, **kwargs):
        return self.objects.order_by('priority')

