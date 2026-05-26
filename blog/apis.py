
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import BlogRepo
from .serializers import BlogSerializer
 
from django.http import JsonResponse
from .forms import *
   
 
class AddBlogApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_blog_form=AddBlogForm(request.POST)
        if add_blog_form.is_valid():
            log=333
            cd=add_blog_form.cleaned_data
            result,message,blog=BlogRepo(request=request).add_blog(**cd)
            if blog is not None:
                context['blog']=BlogSerializer(blog).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   