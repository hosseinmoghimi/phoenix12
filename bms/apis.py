from rest_framework.views import APIView

from utility.log import leolog
from .serializers import FeederSerializer
from utility.constants import FAILED, SUCCEED
from .repo import CommandRepo,FeederRepo
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
                leolog(cd=cd)
                result,message,feeders=FeederRepo(request=request).import_from_json(**cd)
                if feeders is not None:
                    context['feeders']=FeederSerializer(feeders,many=True).data
                  
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


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
    
