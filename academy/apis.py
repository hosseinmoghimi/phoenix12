
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import TableRepo,CourseRepo,TableRepo,checkout_cart
from .serializers import TableSerializer,CourseSerializer
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
  
 