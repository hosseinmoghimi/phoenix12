from django.http import Http404, JsonResponse
from django.shortcuts import render,reverse
from utility.constants import FAILED, SUCCEED 
from core.views import CoreContext, MessageView, PageContext,SearchForm
# Create your views here.
from django.views import View

from utility.calendar import PersianCalendar
from .apps import APP_NAME
from .repo import FileRepo, FolderRepo
from .serializers import FileSerializer, FolderSerializer
from .forms import *
import json


LAYOUT_PARENT = "phoenix/layout.html"
WIDE_LAYOUT_PARENT = "phoenix/wide-layout.html"
TEMPLATE_ROOT = "archive/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    # context['search_form'] = SearchForm()
    # context['search_action'] = reverse(APP_NAME+":search")
    # context['LAYOUT_PARENT'] = LAYOUT_PARENT
    # context['WIDE_LAYOUT_PARENT'] = WIDE_LAYOUT_PARENT
    return context


class HomeView(View):
    def get(self,request,*args, **kwargs):
        return FolderView().get(request=request,pk=1)


class SearchView(View):
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            search_for=search_form.cleaned_data['search_for']
            context['search_for']=search_for
            folders=FolderRepo(request=request).list(search_for=search_for)
            context['folders']=folders
            files=FileRepo(request=request).list(search_for=search_for)
            context['files']=files
        return render(request,TEMPLATE_ROOT+"search.html",context)


class FolderView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        folder=FolderRepo(request=request).folder(*args, **kwargs)
        if folder is None:
            mv=MessageView(request=request)
            mv.title="چنین پوشه ای وجود ندارد."
            mv.body="چنین پوشه ای وجود ندارد."
            return mv.response()
        context['folder']=folder
        folder_s=json.dumps(FolderSerializer(folder).data)
        context['folder_s']=folder_s
        folders=FolderRepo(request=request).list(parent_id=folder.pk).order_by("priority")
        files=folder.files.all().order_by("priority")
        
        context['files']=files
        context['folders']=folders
        files_s=json.dumps(FileSerializer(files,many=True).data)
        folders_s=json.dumps(FolderSerializer(folders,many=True).data)
        context['files_s']=files_s
        context['folders_s']=folders_s


        context['open_folder_form']=OpenFolderForm()
        if request.user.has_perm(APP_NAME+".add_folder"):
            context['create_folder_form']=CreateFolderForm()
        if request.user.has_perm(APP_NAME+".add_file"):
            context['create_file_form']=CreateFileForm()
        return render(request,TEMPLATE_ROOT+"folder.html",context)


class FileView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        file=FileRepo(request=request).file(*args, **kwargs)
        if file is None:
            mv=MessageView(request=request)
            mv.title="فایل پیدا نشد"
            mv.body="فایل مورد نظر وجود ندارد."
            return mv.response()
        sw=True
        if False:
            pagepermissions= file.pagepermission_set.all()
            profile=context['profile']
            sw=False
            if request.user.has_perm(APP_NAME+".view_file"):
                sw=True
            if file.is_public:
                sw=True
            if sw==False:
                for pp in pagepermissions:
                    if pp.profile==profile:
                        sw=True
        if not sw:
            mv=MessageView(request=request)
            mv.title="عدم دسترسی"
            mv.body="دسترسی ندارید"
            return mv.response()
        if file is None:
            mv=MessageView(request=request)
            mv.title="چنین فایلی وجود ندارد."
            mv.body="چنین فایلی وجود ندارد."
            return mv.response()
        context['file']=file
        context.update(PageContext(request=request,page=file))
        return render(request,TEMPLATE_ROOT+"file.html",context)


class CreateFolderApi(View):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED,
        }
        create_folder_form=CreateFolderForm(request.POST)
        if create_folder_form.is_valid():
            folder=FolderRepo(request=request).create_folder(**create_folder_form.cleaned_data)
            context['folder']=FolderSerializer(folder).data
            context['result']=SUCCEED
        return JsonResponse(context)


class CreateFileApi(View):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED,
        }
        create_file_form=CreateFileForm(request.POST)
        if create_file_form.is_valid():
            file=FileRepo(request=request).create_file(**create_file_form.cleaned_data)
            context['file']=FileSerializer(file).data
            context['result']=SUCCEED
        return JsonResponse(context)

 