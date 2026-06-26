from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL 
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext,MessageView 

from utility.calendar import PersianCalendar
import json

from .serializers import CourseSerializer 
from .repo import CourseRepo  
 
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='academy/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)

 

class CoursesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        courses =CourseRepo(request=request).list(*args, **kwargs)
        context['courses']=courses
        courses_s=json.dumps(CourseSerializer(courses,many=True).data)
        context['courses_s']=courses_s
 
        context[WIDE_LAYOUT]=True
        if request.user.has_perm(APP_NAME+".add_course"):
            context['add_course_form']=AddCourseForm()
            from market.views import SupplierRepo
            suppliers=SupplierRepo(request=request).list()
            context['suppliers']=suppliers
        return render(request,TEMPLATE_ROOT+"courses.html",context) 
    
 


class CourseView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        from market.views import CustomerRepo,CartItemRepo,ShopSerializer
        course =CourseRepo(request=request).course(*args, **kwargs) 
        context['course']=course
        course_s=json.dumps(CourseSerializer(course,many=False).data)
        context['course_s']=course_s

        shops=course.shops.all()
        shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        context['shops_s']=shops_s

  
 

        context[WIDE_LAYOUT]=True
        # context['NOT_NAVBAR']=True
        # context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"course.html",context) 
 
 