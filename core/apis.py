# from core.serializers import PageBriefSerializer, PageCommentSerializer, PageDecodeSerializer, PageDownloadSerializer, PageImageSerializer, PageLikeSerializer, PageLinkSerializer, PagePermissionSerializer, PageSerializer, PageTagSerializer, ParameterSerializer, TagSerializer
from rest_framework.views import APIView
from django.http import JsonResponse
from .forms import *
# from .repo import ContactMessageRepo, PageCommentRepo, PageLinkRepo, PagePermissionRepo, PageRepo, PageTagRepo,  ParameterRepo,PageDownloadRepo,PageImageRepo
from .repo import  PageRepo 
from .serializers import  PageSerializer
from utility.constants import SUCCEED, FAILED
from utility.utils import str_to_html
from core.views import PageBriefSerializer
  
class SetPagePriorityApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        result=FAILED
        message=""
        log=111
        context['result']=FAILED
        if request.method=='POST':
            log=222
            set_page_priority_form=SetPagePriorityForm(request.POST)
            if set_page_priority_form.is_valid():
                log=333
                cd=set_page_priority_form.cleaned_data
                priority,message,result=PageRepo(request=request).set_priority(**cd)
                if priority is not None:
                    context['priority']=priority
        context['message']=message
        context['result']=result
        context['log']=log
        return JsonResponse(context)


    
class AddRelatedPageApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_related_page_form=AddRelatedPageForm(request.POST)
            if add_related_page_form.is_valid():
                page_id = add_related_page_form.cleaned_data['page_id']
                related_page_id = add_related_page_form.cleaned_data['related_page_id']
                bidirectional = add_related_page_form.cleaned_data['bidirectional']
                add_or_remove = add_related_page_form.cleaned_data['add_or_remove']
                related_page = PageRepo(request=request).add_related_page(add_or_remove=add_or_remove,page_id=page_id, bidirectional=bidirectional, related_page_id=related_page_id)
                if related_page is not None:
                    log = 4
                    context['related_page'] = PageBriefSerializer(related_page).data
                    context['result'] = SUCCEED
        context['log']=log
        return JsonResponse(context)

class SetPageThumbnailHeaderApi(APIView):
    def post(self, request, *args, **kwargs):
        log = 1
        context = {}
        context['result'] = FAILED
        if request.method == 'POST':
            log += 1
            SetThumbnailHeaderForm_ = SetPageThumbnailHeaderForm(request.POST, request.FILES)
            if SetThumbnailHeaderForm_.is_valid():
                log += 1
                cd=SetThumbnailHeaderForm_.cleaned_data
                page_id = cd['page_id']
                clear_thumbnail = cd['clear_thumbnail']
                clear_header = cd['clear_header']
                title = cd['title']
                color = cd['color']
                thumbnail = None
                header = None
                if 'thumbnail' in request.FILES:
                    thumbnail = request.FILES['thumbnail']
                if 'header' in request.FILES:
                    header = request.FILES['header']
                
                page = PageRepo(request=request).set_thumbnail_header(
                    clear_thumbnail=clear_thumbnail,
                    color=color,
                    clear_header=clear_header,
                    page_id=page_id,
                    title=title,
                    thumbnail=thumbnail,
                    header=header
                    )
                if page is not None:
                    context['page'] = PageSerializer(page).data
                    context['result'] = SUCCEED
        context['log'] = log
        return JsonResponse(context)



class TogglePageLikeApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=1
        if request.method=='POST':
            log+=1
            add_related_page_form=TogglePageLikeForm(request.POST)
            if add_related_page_form.is_valid():
                log+=1
                page_id = add_related_page_form.cleaned_data['page_id']
                (my_like,likes_count) = PageRepo(request=request).toggle_like(page_id=page_id)
                context['my_like'] = my_like
                context['likes_count'] = likes_count
                context['result'] = SUCCEED
        context['log']=log
        return JsonResponse(context)
        