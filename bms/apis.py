from rest_framework.views import APIView

from utility.log import leolog
from .serializers import FeederSerializer
from utility.constants import FAILED, SUCCEED
from .repo import CommandRepo
from .forms import *
from django.http import JsonResponse

class ExportApi(APIView):
    def post(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            form1=ExecuteCommandForm(request.POST)
            if form1.is_valid():
                log=3
                cd=form1.cleaned_data
                # result=CommandRepo(request=request).execute_command1(**cd)
                location=None
                if location is not None:
                    log=4
                    location_s=FeederSerializer(location).data
                    return JsonResponse({'result':SUCCEED,'location':location_s})
        return JsonResponse({'result':FAILED,'log':log})
    

class ExecuteCommandApi(APIView):
     def post(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            form1=ExecuteCommandForm(request.POST)
            if form1.is_valid():
                log=3
                cd=form1.cleaned_data
                result,registers,message=CommandRepo(request=request).execute_command(**cd)
                if result is not None:
                    return JsonResponse({'result':SUCCEED,'registers':registers})
        return JsonResponse({'result':FAILED,'log':log})
    
