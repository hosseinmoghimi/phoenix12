# from core.serializers import PageBriefSerializer, PageCommentSerializer, PageDecodeSerializer, PageDownloadSerializer, PageImageSerializer, PageLikeSerializer, PageLinkSerializer, PagePermissionSerializer, PageSerializer, PageTagSerializer, ParameterSerializer, TagSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
# from .repo import ContactMessageRepo, PageCommentRepo, PageLinkRepo, PagePermissionRepo, PageRepo, PageTagRepo,  ParameterRepo,PageDownloadRepo,PageImageRepo
from .repo import LikeRepo,CommentRepo,LinkRepo,DownloadRepo,ImageRepo, TagRepo,PagePrintRepo
from .serializer import  CommentSerializer,LinkSerializer,DownloadSerializer,ImageSerializer, TagSerializer,PagePrintSerializer
from utility.constants import SUCCEED, FAILED
from utility.utils import str_to_html
from .views import AreaRepo,AreaSerializer,LocationRepo,LocationSerializer
 

 

class AddPagePrintApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result=FAILED
        message=''
        if request.method == 'POST':
            log += 1
            add_page_print_form = AddPagePrintForm(request.POST)
            if add_page_print_form.is_valid():
                log += 1
                cd=add_page_print_form.cleaned_data
                page_id = cd['page_id']
                type = cd['type']
                
                
                result,message,page_print = PagePrintRepo(request=request).add_page_print(
                    page_id=page_id,
                    type=type,
                     printed=True
                    )
                if result==SUCCEED:
                    context['page_print'] = PagePrintSerializer(page_print).data
        context['message'] = message
        context['result'] = result
        context['log'] = log
        return JsonResponse(context)
    
class AddLocationApi(APIView):
    def post(self,request,*args, **kwargs):
        log=1
        if request.method=='POST':
            log=2
            add_location_form=AddLocationForm(request.POST)
            if add_location_form.is_valid():
                log=3
                location=add_location_form.cleaned_data['location']
                title=add_location_form.cleaned_data['title']
                page_id=add_location_form.cleaned_data['page_id']
                result,message,location=LocationRepo(request=request).add_location(location=location,title=title,page_id=page_id)
                
                if location is not None:
                    log=4
                    location_s=LocationSerializer(location).data
                    return JsonResponse({'result':SUCCEED,'location':location_s})
        return JsonResponse({'result':FAILED,'log':log})
    

class AddAreaApi(APIView):
    def post(self,request):
        context={'result':FAILED}
        log=1
        user=request.user
        if request.method=='POST':
            log=2
            add_area_form=AddAreaForm(request.POST)
            if add_area_form.is_valid():
                log=3
                
                title=add_area_form.cleaned_data['title']
                code=add_area_form.cleaned_data['code']
                area=add_area_form.cleaned_data['area']
                color=add_area_form.cleaned_data['color']
              
                area=AreaRepo(request=request).add_area(
                    title=title,
                    code=code,
                    color=color,
                    area=area,
                )
                
                if area is not None:
                    log=4
                    context['area']=AreaSerializer(area).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)
    
    
class AddPageLocationApi(APIView):
    def post(self,request,*args, **kwargs):
        log=1
        context={}
        message='پاراکتر های ورودی معتبر نمی باشند.'
        result=FAILED
        if request.method=='POST':
            log=2
            add_location_form=AddPageLocationForm(request.POST)
            if add_location_form.is_valid():
                log=3 
                cd=add_location_form.cleaned_data
                location=LocationRepo(request=request).add_page_location(**cd)
                if location is not None:
                    log=4
                    result=SUCCEED
                    location=LocationSerializer(location).data
                    context['location']=location
        context['log']=log
        context['result']=result
        context['message']=message
        return JsonResponse(context)
     

class AddImageApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            add_page_download_form = AddImageForm(request.POST, request.FILES)
            if add_page_download_form.is_valid():
                log += 1
                cd=add_page_download_form.cleaned_data
                page_id = cd['page_id']
                title = cd['title']
                image = request.FILES['image']
                
                result,message,image = ImageRepo(request=request).add_image(
                    page_id=page_id,
                    title=title,
                    image=image,
                    )
                if result==SUCCEED and image is not None:
                    context['image'] = ImageSerializer(image).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)
    
 
class ToggleLikeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_related_page_form=TogglePageLikeForm(request.POST)
            if add_related_page_form.is_valid():
                log+=1
                page_id = add_related_page_form.cleaned_data['page_id']
                (my_like,likes_count) = LikeRepo(request=request).toggle_like(page_id=page_id)
                context['my_like'] = my_like
                context['likes_count'] = likes_count
                context['result'] = SUCCEED
        context['log']=log
        return JsonResponse(context)
        
class AddCommentApi(APIView):
    def post(self,request,*args, **kwargs):
        result,message,comment=FAILED,"",None
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_page_comment_form=AddPageCommentForm(request.POST)
            if add_page_comment_form.is_valid():
                log+=1
                parent_id = add_page_comment_form.cleaned_data['parent_id']
                page_id = add_page_comment_form.cleaned_data['page_id']
                comment = add_page_comment_form.cleaned_data['comment']
                (result,message,comment) = CommentRepo(request=request).add_comment(page_id=page_id,comment=comment,parent_id=parent_id)
                if result==SUCCEED:
                    context['comment'] = CommentSerializer(comment).data
        context['result'] = result
        context['message'] = message
        context['log']=log
        return JsonResponse(context)
    
         
class AddTagApi(APIView):
    def post(self,request,*args, **kwargs):
        result,message,comment=FAILED,"",None
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_tag_form=AddTagForm(request.POST)
            if add_tag_form.is_valid():
                log+=1
                page_id = add_tag_form.cleaned_data['page_id']
                title = add_tag_form.cleaned_data['title']
                (result,message,tags) = TagRepo(request=request).add_tag(page_id=page_id,title=title)
                if result==SUCCEED:
                    context['tags'] = TagSerializer(tags,many=True).data
        context['result'] = result
        context['message'] = message
        context['log']=log
        return JsonResponse(context)
    
           
class DeleteCommentApi(APIView):
    def post(self,request,*args, **kwargs):
        result,message,comment=FAILED,"",None
        context={}
        log=1
        if request.method=='POST':
            log+=1
            delete_page_comment_form=DeletePageCommentForm(request.POST)
            if delete_page_comment_form.is_valid():
                log+=1
                comment_id = delete_page_comment_form.cleaned_data['comment_id']
                (result,message) = CommentRepo(request=request).delete_page_comment(comment_id=comment_id)
                 
        context['result'] = result
        context['message'] = message
        context['log']=log
        return JsonResponse(context)
        
            
class AddLinkApi(APIView):
    def post(self,request,*args, **kwargs):
        result,message,comment=FAILED,"",None
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_link_form=AddLinkForm(request.POST)
            if add_link_form.is_valid():
                log+=1 
                (result,message,link) = LinkRepo(request=request).add_link(**add_link_form.cleaned_data)
                if result==SUCCEED:
                    context['link'] = LinkSerializer(link).data
        context['result'] = result
        context['message'] = message
        context['log']=log
        return JsonResponse(context)
    
       

      
class AddDownloadApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        result,message,download=FAILED,"",None
        if request.method == 'POST':
            log += 1
            add_page_download_form = AddDownloadForm(request.POST, request.FILES)
            if add_page_download_form.is_valid():
                log += 1
                cd=add_page_download_form.cleaned_data
                page_id = cd['page_id']
                title = cd['title']
                try:
                    file = request.FILES['file1']
                except:
                    
                    context['log'] = log
                    context['result'] = FAILED
                    context['message'] = 'فایل را انتخاب کنید'
                    return JsonResponse(context)
                result,message,download = DownloadRepo(request=request).add_download(
                    page_id=page_id,
                    title=title,
                    file=file,
                    )
                if download is not None:
                    context['download'] = DownloadSerializer(download).data
        context['log'] = log
        context['result'] = result
        context['message'] = message
        return JsonResponse(context)
     
       