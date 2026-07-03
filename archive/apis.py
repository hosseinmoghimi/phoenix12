from django.http import JsonResponse
from rest_framework.views import APIView
from archive.repo import FolderRepo
from core.apis import SUCCEED,FAILED
from archive.forms import *
from archive.serializers import FolderSerializer,FileSerializer
class OpenFolderApi(APIView):
    def post(self,request,*args, **kwargs):
        context={
            'result':FAILED,
        }
        open_folder_form=OpenFolderForm(request.POST)
        if open_folder_form.is_valid():
            folder_id=open_folder_form.cleaned_data['folder_id']
            folder_repo=FolderRepo(request=request)
            folder=folder_repo.folder(folder_id=folder_id)
            folders=folder.childs.all()
            context['folder']=FolderSerializer(folder).data
            context['folders']=FolderSerializer(folders,many=True).data
            files=FileSerializer(folder.files.all(),many=True).data
            context['files']=files
            context['result']=SUCCEED
        return JsonResponse(context)