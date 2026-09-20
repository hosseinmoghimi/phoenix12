from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from .repo import FoodRepo
from .serializers import FoodSerializer
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext,MessageView 

from utility.calendar import PersianCalendar
import json

from .serializers import FoodSerializer
from .repo import FoodRepo
from .enums import *

from utility.enums import UnitNameEnum
from utility.log import leolog 

LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='restaurant/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def AddFoodContext(request,*args, **kwargs):
    context={}
    context['add_food_form']=AddFoodForm()
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


class SettingsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"settings.html",context)

class FoodView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        food =FoodRepo(request=request).food(*args, **kwargs)
        context['food']=food
         
 
   
        return render(request,TEMPLATE_ROOT+"food.html",context) 
    
     
class FoodsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        foods =FoodRepo(request=request).list(*args, **kwargs)
        context['foods']=foods
        
        foods_s=json.dumps(FoodSerializer(foods,many=True).data)
        context['foods_s']=foods_s
        if request.user.has_perm(APP_NAME+'.add_food'):
            context.update(AddFoodContext(request=request))
        return render(request,TEMPLATE_ROOT+"foods.html",context) 
     