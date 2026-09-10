
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import FoodRepo
from .serializers import FoodSerializer
from django.http import JsonResponse
from .forms import *
    
     

class AddFoodApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_food_form=AddFoodForm(request.POST)
        if add_food_form.is_valid():
            log=333
            cd=add_food_form.cleaned_data
            result,message,food=FoodRepo(request=request).add_food(**cd)
            if food is not None:
                context['food']=FoodSerializer(food).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
   