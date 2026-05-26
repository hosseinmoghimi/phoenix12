from .serializers import ParameterSerializer,PictureSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
from .repo import ParameterRepo,PictureRepo
from utility.constants import SUCCEED, FAILED
from utility.utils import str_to_html
 
class SetParameterApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result = FAILED
        message=''
        if request.method == 'POST':
            log += 1
            set_parameter_form = SetParameterForm(request.POST)
            if set_parameter_form.is_valid():
                log += 1
                cd=set_parameter_form.cleaned_data 
                app_name = cd['app_name']
                name = cd['name']
                value = cd['value']
                
                result,message,parameter = ParameterRepo(request=request,app_name=app_name).set_parameter(
                    name=name,
                    app_name=app_name,
                    value=value,
                    )
                if result==SUCCEED:
                    context['parameter'] = ParameterSerializer(parameter).data
        context['log'] = log
        context['message'] = message
        context['result'] = result
        return JsonResponse(context)

class GetParametersApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result = FAILED
        if request.method == 'POST':
            log =2
            get_parameters_form = GetParametersForm(request.POST)
            if get_parameters_form.is_valid():
                log =3
                cd=get_parameters_form.cleaned_data
                app_name = cd['app_name']
                parameters=ParameterRepo(request=request,app_name=app_name).list()
                parameters=ParameterSerializer(parameters,many=True).data
                context['parameters']=parameters
                result = SUCCEED

        context['result'] = result
        context['log'] = log
        return JsonResponse(context)



class GetParametersAndPicturesApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result = FAILED
        if request.method == 'POST':
            log =2
            get_parameters_form = GetParametersForm(request.POST)
            if get_parameters_form.is_valid():
                log =3
                cd=get_parameters_form.cleaned_data
                app_name = cd['app_name']
                parameters=ParameterRepo(request=request,app_name=app_name).list()
                parameters=ParameterSerializer(parameters,many=True).data
                pictures=PictureRepo(request=request,app_name=app_name).list()
                pictures=PictureSerializer(pictures,many=True).data
                context['parameters']=parameters
                context['pictures']=pictures
                result = SUCCEED

        context['result'] = result
        context['log'] = log
        return JsonResponse(context)

