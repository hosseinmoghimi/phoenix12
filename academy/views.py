from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL 
from django.views import View
from .forms import *
from .apps import APP_NAME
from core.views import CoreContext,MessageView,PageContext

from utility.calendar import PersianCalendar
import json

from .serializers import CourseSerializer,WordSerializer
from .repo import CourseRepo,WordRepo
 
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

class SearchView(View):
    def post(self,request,*args, **kwargs):
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            search_for=search_form.cleaned_data['search_for']
            context=getContext(request=request)
           

            words=WordRepo(request=request).list(search_for=search_for).order_by('title')

            context['search_for']=search_for
            words_s=json.dumps(WordSerializer(words,many=True).data)
            context['words_s']=words_s
            context['words']=words
        
        return render(request,TEMPLATE_ROOT+"search.html",context)

 
class GetJsonBackupView(View):
    def get(self,request,*args, **kwargs):
        from django.http import JsonResponse
        origin_words=WordRepo(request=request).list()
        json_data={'words':[]}
        for word in origin_words:
            data={} 
            data['id']=word.id
            data['title']=word.title
            data['parent_id']=word.parent_id
            data['thumbnail_origin']=str(word.thumbnail_origin)
            json_data['words'].append(data)


        return JsonResponse(json_data,safe=False)
 

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
 


class SettingsView(View):
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
        return render(request,TEMPLATE_ROOT+"settings.html",context) 
 

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
 

class WordView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        
        word =WordRepo(request=request).word(*args, **kwargs) 
        if word is None:
            words=WordRepo(request=request).list(parent_id=None).order_by('title')
        else:
            context.update(PageContext(request=request,page=word))
            words=WordRepo(request=request).list(parent_id=word.id).order_by('title')
            context['word']=word
            word_s=json.dumps(WordSerializer(word,many=False).data)
            context['word_s']=word_s

        words_s=json.dumps(WordSerializer(words,many=True).data)
        context['words_s']=words_s
        context['words']=words
 
        if request.user.has_perm(APP_NAME+".add_word"):
            context['add_word_form']=AddWordForm()
        return render(request,TEMPLATE_ROOT+"word.html",context) 
 

class WordsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
         

        words=WordRepo(request=request).list().order_by('title')
        words_s=json.dumps(WordSerializer(words,many=True).data)
        context['words_s']=words_s
        context['words']=words
 
   
        return render(request,TEMPLATE_ROOT+"words.html",context) 
 
 

