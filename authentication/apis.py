
from utility.constants import FAILED,SUCCEED
from rest_framework.views import APIView
import json
from utility.calendar import PersianCalendar
from utility.log import leolog
from .repo import PersonRepo,PersonRepo,ClipBoardItemRepo,MyLinkRepo
from .serializers import PersonSerializer,MyLinkSerializer,ClipBoardItemSerializer
from django.http import JsonResponse
from .forms import *
   

class ChangePasswordApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        change_password_form=ChangePasswordForm(request.POST)
        if change_password_form.is_valid():
            log=333
            cd=change_password_form.cleaned_data
            (request,user,result,message)=PersonRepo(request=request).change_password(request,**cd)
            if user is not None:
                person=PersonRepo(request=request).me
                if person is not None:
                    context['person']=PersonSerializer(person).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
class AddPersonApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        add_person_form=AddPersonForm(request.POST)
        if add_person_form.is_valid():
            log=333
            cd=add_person_form.cleaned_data
            result,message,person=PersonRepo(request=request).add_person(**cd)
            if person is not None:
                context['person']=PersonSerializer(person).data
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class SelectPersonApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        select_person_form=SelectPersonForm(request.POST)
        if select_person_form.is_valid():
            log=333
            cd=select_person_form.cleaned_data
            person=PersonRepo(request=request).person(**cd)
            if person is not None:
                context['person']=PersonSerializer(person).data
                result=SUCCEED
                message='موفق'
            else:
                message='شخص پیدا نشد.'
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class EditPersonApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        edit_person_form=EditPersonForm(request.POST)
        if edit_person_form.is_valid():
            log=333
            cd=edit_person_form.cleaned_data
            result,message,person=PersonRepo(request=request).edit_person(**cd)
            if person is not None:
                context['person']=PersonSerializer(person).data
                result=SUCCEED
                message='موفق'
            else:
                message='شخص پیدا نشد.'
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 

class SelectUserApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        select_person_form=SelectUserForm(request.POST)
        if select_person_form.is_valid():
            log=333
            cd=select_person_form.cleaned_data
            user=PersonRepo(request=request).user(**cd)
            if user is not None:
                context['username']=user.username
                result=SUCCEED
                message='موفق'
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)
 
class SelectProfileApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED 
        log=222
        from utility.message import INVALID_FORM_VALUE_MESSAGE
        message=INVALID_FORM_VALUE_MESSAGE
        select_profile_form=SelectProfileForm(request.POST)
        if select_profile_form.is_valid():
            log=333
            cd=select_profile_form.cleaned_data
            profile=PersonRepo(request=request).profile(**cd)
            if profile is not None:
                context['profile']=ProfileSerializer(profile).data
                message='موفق'
                result=SUCCEED
        context['result']=result
        context['message']=message
        context['log']=log
        return JsonResponse(context)
 


class AddClipBoardItemApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result = FAILED
        message=''
        if request.method == 'POST':
            log += 1
            add_to_clipboard_form = AddToClipBoradForm(request.POST)
            if add_to_clipboard_form.is_valid():
                log += 1
                cd=add_to_clipboard_form.cleaned_data 
                text = cd['text']
                name = cd['name']
                
                result = ClipBoardItemRepo(request=request,).add_clipboard_item(
                    text=text,
                    name=name,
                    )
                 
        context['log'] = log
        context['message'] = message
        context['result'] = result
        return JsonResponse(context)


class DeleteMyLinkApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result = FAILED
        message=''
        if request.method == 'POST':
            log += 1
            delete_my_link_form = DeleteMyLinkForm(request.POST)
            if delete_my_link_form.is_valid():
                log += 1
                cd=delete_my_link_form.cleaned_data 
                my_link_id = cd['my_link_id']
                
                result,my_links = MyLinkRepo(request=request).delete_my_link(
                    my_link_id=my_link_id,
                    )
                context['my_links']=MyLinkSerializer(my_links,many=True).data
                 
        context['log'] = log
        context['message'] = message
        context['result'] = result
        return JsonResponse(context)



class AddMyLinkApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result = FAILED
        message=''
        if request.method == 'POST':
            log += 1
            add_my_link_form = AddMyLinkForm(request.POST)
            if add_my_link_form.is_valid():
                log += 1
                cd=add_my_link_form.cleaned_data 
                
                result,my_links = MyLinkRepo(request=request).add_my_link(
                    **cd
                    )
                context['my_links']=MyLinkSerializer(my_links,many=True).data
                 
        context['log'] = log
        context['message'] = message
        context['result'] = result
        return JsonResponse(context)


class ClearAllClipBoardItemsApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result = FAILED
        message=''
        if request.method == 'POST':
            log += 1
            clear_all_clipboard_items_form = ClearAllClipBoradItemForm(request.POST)
            if clear_all_clipboard_items_form.is_valid():
                log += 1
                cd=clear_all_clipboard_items_form.cleaned_data 
               
                
                result = ClipBoardItemRepo(request=request,).clear_all_clipboard_items()
                 
        context['log'] = log
        context['message'] = message
        context['result'] = result
        return JsonResponse(context)

