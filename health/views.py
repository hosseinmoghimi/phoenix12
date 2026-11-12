from django.shortcuts import render,redirect
from utility.constants import INDEX_FOR_ALL_CHOICES
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL
from accounting.views import ProductContext
from .forms import *
from .apps import APP_NAME
from .serializers import DrugSerializer
from .repo import DrugRepo
 
import json
from .enums import *
from django.views import View
from core.views import CoreContext,leolog 
from utility.views import RegionRepo
from .serializers import DrugSerializer
from utility.views import MessageView
from utility.repo import ParameterRepo,PictureRepo

TEMPLATE_ROOT="health/"
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"


LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='health/'



def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

 
       

class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context[WIDE_LAYOUT]=True
         

        return render(request,TEMPLATE_ROOT+"index.html",context) 
 

class DrugView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drug =DrugRepo(request=request).drug(*args, **kwargs)
        context[WIDE_LAYOUT]=False
        context['drug']=drug
        from accounting.views import ProductContext
        context.update(ProductContext(request=request,product=drug,*args, **kwargs))
        return render(request,TEMPLATE_ROOT+"drug.html",context) 


class DrugsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        drugs =DrugRepo(request=request).list(*args, **kwargs)
   
        context[WIDE_LAYOUT]=True
        context['drugs']=drugs
        drugs_s=json.dumps(DrugSerializer(drugs,many=True).data)
        context['drugs_s']=drugs_s
        return render(request,TEMPLATE_ROOT+"drugs.html",context) 

