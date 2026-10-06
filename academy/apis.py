
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import CourseRepo,WordRepo
from .serializers import CourseSerializer,WordSerializer
from django.http import JsonResponse
from .forms import *
    
    
class AddCourseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_course_form=AddCourseForm(request.POST)
        if add_course_form.is_valid():
            log=333
            cd=add_course_form.cleaned_data
            result,message,course=CourseRepo(request=request).add_course(**cd)
            if course is not None:
                context['course']=CourseSerializer(course).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)

 
class ImportFromJsonApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
       
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            import_from_excel_form=ImportFromJsonForm(request.POST,request.FILES)
            if import_from_excel_form.is_valid():
                log=333
                
                json_file = request.FILES['file1']
                cd=import_from_excel_form.cleaned_data
                cd['json_file']=json_file
                result,message,words=WordRepo(request=request).import_from_json(**cd)
                if words is not None:
                    context['words']=WordSerializer(words,many=True).data
                  
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)        
    
    
class DeleteAllWordsApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
       
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            delete_all_words_form=DeleteAllWordsForm(request.POST,request.FILES)
            if delete_all_words_form.is_valid():
                log=333
                
                cd=delete_all_words_form.cleaned_data
                result,message=WordRepo(request=request).delete_all_words(**cd) 
                  
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)        
    
    
class AddWordApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_word_form=AddWordForm(request.POST)
        if add_word_form.is_valid():
            log=333
            cd=add_word_form.cleaned_data
            result,message,word=WordRepo(request=request).add_word(**cd)
            if word is not None:
                context['word']=WordSerializer(word).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
  
 