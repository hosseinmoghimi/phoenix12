from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL,CURRENCY,VUE_VERSION_3,VUE_VERSION_2
from authentication.repo import PersonRepo
from utility.repo import ParameterRepo,PictureRepo
from django.views import View
from .forms import *
from .serializer import CommentSerializer,LinkSerializer,DownloadSerializer,PagePrintSerializer
from .apps import APP_NAME
from django.http import Http404
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from utility.log import leolog
from django.utils import timezone
from core.views import MessageView,CoreContext,PageBriefSerializer,AddRelatedPageForm
from .repo import LikeRepo,CommentRepo,LinkRepo,DownloadRepo, TagRepo,PagePrintRepo
import json


from .repo import ImageRepo,LocationRepo,AreaRepo
from .serializer import ImageSerializer,LocationSerializer,AreaSerializer,TagSerializer
       

LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='attachments/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"

def PageLikesContext(request,page,person,*args, **kwargs):
    context={}
    like_repo = LikeRepo(request=request) 
    my_like = like_repo.my_like(page=page)
    likes_count = like_repo.likes_count(page=page)
    context['my_like']=my_like
    context['likes_count']=likes_count  
    if person is not None:
        context['toggle_page_like_form']=TogglePageLikeForm()
    return context
 
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
 
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
 
def PageCommentsContext(request,page,person,*args, **kwargs):
    context={}
    comment_repo = CommentRepo(request=request) 
    comments=comment_repo.list(page_id=page.id)
    comments_s=json.dumps(CommentSerializer(comments,many=True).data)
    context['comments']=comments  
    context['comments_s']=comments_s  
    if person is not None:
        if request.user.has_perm(APP_NAME+'.add_comment'):
            context['add_comment_form']=AddPageCommentForm()
            context['delete_comment_form']=DeletePageCommentForm()
    return context
 
def PagPrintsContext(request,page,person,*args, **kwargs):
    context={}
    page_print_repo = PagePrintRepo(request=request) 
    page_prints=page_print_repo.list(page_id=page.id)
    page_prints_s=json.dumps(PagePrintSerializer(page_prints,many=True).data)
    context['page_prints']=page_prints  
    context['page_prints_s']=page_prints_s  
    # if person is not None:
    #     if request.user.has_perm(APP_NAME+'.add_pageprint'):
    #         context['add_page_print_form']=AddPagePrintForm()
    return context
 
def PageLinksContext(request,page,person,*args, **kwargs):
    context={}
    link_repo = LinkRepo(request=request) 
    links=link_repo.list(page_id=page.id)
    links_s=json.dumps(LinkSerializer(links,many=True).data)
    context['links']=links  
    context['links_s']=links_s  
    if person is not None:
        if person.user.has_perm(APP_NAME+'.add_link'):
            context['add_link_form']=AddLinkForm()
    return context

def PageDownloadsContext(request,page,person,*args, **kwargs):
    context={}
    download_repo = DownloadRepo(request=request) 
    downloads=download_repo.list(page_id=page.id)
    downloads_s=json.dumps(DownloadSerializer(downloads,many=True).data)
    context['downloads']=downloads  
    context['downloads_s']=downloads_s  
    if person is not None:
        if person.user.has_perm(APP_NAME+'.add_download'):
            context['add_download_form']=AddDownloadForm()
    return context


def PageTagsContext(request,page,person,*args, **kwargs):
    context={}
    tag_repo = TagRepo(request=request) 
    tags=tag_repo.list(page_id=page.id)
    tags_s=json.dumps(TagSerializer(tags,many=True).data)
    context['tags']=tags  
    context['tags_s']=tags_s  
    if person is not None:
        if person.user.has_perm(APP_NAME+'.add_tag'):
            context['add_tag_form']=AddTagForm()
    return context


def PageRelatedContext(request,page,*args, **kwargs):
    context={}
    related_pages = page.related_pages.all()
    
    context['related_pages'] = related_pages
    context['related_pages_s'] = json.dumps(PageBriefSerializer(related_pages, many=True).data)
    if request.user.has_perm(APP_NAME,'change_page'):
        context['add_related_page_form'] = AddRelatedPageForm()

    return context



def PageImagesContext(request,page,*args, **kwargs):
    context={}
    image_repo = ImageRepo(request=request) 
    images=image_repo.list(page_id=page.id)
    images_s=json.dumps(ImageSerializer(images,many=True).data)
    context['images']=images  
    context['images_s']=images_s  
    if request.user.has_perm(APP_NAME+'.add_image') :
        context['add_image_form']=AddImageForm() 
    return context


def PageLocationsContext(request,page,*args, **kwargs):
    context={}
    location_repo = LocationRepo(request=request) 
    locations=page.locations.all()
    locations_s=json.dumps(LocationSerializer(locations,many=True).data)
    context['locations']=locations  
    context['locations_s']=locations_s  

    if request.user.has_perm(APP_NAME+'.add_location'):
        all_locations=location_repo.list()
        context['all_locations']=all_locations  
        context['add_page_location_form']=AddPageLocationForm()  
        context['add_location_form']=AddLocationForm()
    return context


class DownloadView(View):
    def get(self, request, *args, **kwargs): 
        me = PersonRepo(request=request).me
        download = DownloadRepo(request=request).download(*args, **kwargs)
        if download is None or (me is None and not download.is_open):
            pass
        elif request.user.has_perm("attachments.change_download") or download.is_open or me in download.profiles.all():
            file_path = str(download.file.path)
            # return JsonResponse({'download:':str(file_path)})
            import os
            from django.http import HttpResponse
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(
                        fh.read(), content_type="application/force-download")
                    response['Content-Disposition'] = 'inline; filename=  '+ os.path.basename(file_path)
                    download.download_counter += 1
                    download.save()
                    return response
                    
        # if self.access(request=request,*args, **kwargs) and document is not None:
        #     return document.download_response()
        # from utility.views import MessageView
        from core.views import MessageView
        message_view = MessageView()
        message_view.links = []
        message_view.message_color = 'warning'
        message_view.has_home_link = True
        message_view.header_color = "rose"
        message_view.message_icon = ''
        message_view.header_icon = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i>'
        body = ' شما مجوز دسترسی به این صفحه را ندارید.'
        title = 'دسترسی غیر مجاز'
        message_view = MessageView(title=title,body=body)
        if download is None:
            message_view.body = 'موقعیت مورد نظر شما پیدا نشد.'
            message_view.title = 'موقعیت مورد نظر پیدا نشد.'
        else:
            from .models import Link
            message_view.links.append(Link(title='تلاش مجدد', color="warning",
                                  icon_material="apartment", url=download.get_download_url))

        return message_view.get(request=request)
      
def SearchContext(request,search_for,*args, **kwargs):
    context={}
    WAS_FOUND=False


    tags=TagRepo(request=request).list(search_for=search_for)
    if len(tags)>0:
        context['tags']=tags
        context['tags_s']=json.dumps(TagSerializer(tags,many=True).data)
        WAS_FOUND=True


    downloads=DownloadRepo(request=request).list(search_for=search_for)
    if len(downloads)>0:
        context['downloads']=downloads
        context['downloads_s']=json.dumps(DownloadSerializer(downloads,many=True).data)
        WAS_FOUND=True


    links=LinkRepo(request=request).list(search_for=search_for)
    if len(links)>0:
        context['links']=links
        context['links_s']=json.dumps(LinkSerializer(links,many=True).data)
        WAS_FOUND=True

    images=ImageRepo(request=request).list(search_for=search_for)
    if len(images)>0:
        context['images']=images
        context['images_s']=json.dumps(ImageSerializer(images,many=True).data)
        WAS_FOUND=True


          

    if WAS_FOUND:
               context['WAS_FOUND']=WAS_FOUND
    return context
  
      
class IndexView(View):
    def get(self, request, *args, **kwargs): 
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+'index.html',context)
        
      


class TagView(View):
    def get(self, request, *args, **kwargs):
        me = PersonRepo(request=request).me
        tag = TagRepo(request=request).tag(*args, **kwargs)
        if tag is None:
            title='تگ پیدا نشد.'
            body='تگ پیدا نشد.'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        context=getContext(request=request)
        context['tag']=tag
        page_tags=tag.pages.all()
        context['page_tags']=page_tags
        pages=tag.pages.all()
        pages_s=json.dumps(PageBriefSerializer(pages,many=True).data)
        context['pages']=pages
        context['pages_s']=pages_s
        context['expand_pages']=True

        return render(request,TEMPLATE_ROOT+"tag.html",context)
       
       

class TagsView(View):
    def get(self, request, *args, **kwargs):
        me = PersonRepo(request=request).me
        tags = TagRepo(request=request).list(*args, **kwargs)
        tags_s=json.dumps(TagSerializer(tags,many=True).data)
        context=getContext(request=request)
        context['tags']=tags
        context['tags_s']=tags_s

        return render(request,TEMPLATE_ROOT+"tags.html",context)
       
      
      
class LinksView(View):
    def get(self, request, *args, **kwargs): 
        context=getContext(request=request)
        links=LinkRepo(request=request).list(*args, **kwargs)
        context['links']=links
        links_s=json.dumps(LinkSerializer(links,many=True).data)
        context['links_s']=links_s
        return render(request,TEMPLATE_ROOT+'links.html',context)
        
      

       

       
class DownloadsView(View):
    def get(self, request, *args, **kwargs): 
        context=getContext(request=request)
        downloads=DownloadRepo(request=request).list(*args, **kwargs)
        context['downloads']=downloads
        downloads_s=json.dumps(DownloadSerializer(downloads,many=True).data)
        context['downloads_s']=downloads_s
        return render(request,TEMPLATE_ROOT+'downloads.html',context)
        
      

       
class CommentsView(View):
    def get(self, request, *args, **kwargs): 
        context=getContext(request=request)
        comments=CommentRepo(request=request).list(*args, **kwargs)
        context['comments']=comments
        comments_s=json.dumps(CommentSerializer(comments,many=True).data)
        context['comments_s']=comments_s
        return render(request,TEMPLATE_ROOT+'comments.html',context)
        
      

class ImagesView(View):
    def get(self, request, *args, **kwargs): 
        context=getContext(request=request)
        images=ImageRepo(request=request).list(*args, **kwargs)
        context['images']=images
        images_s=json.dumps(ImageSerializer(images,many=True).data)
        context['images_s']=images_s
        return render(request,TEMPLATE_ROOT+'images.html',context)
        
      
  
class ImageView(View):
    def get(self, request, *args, **kwargs):
        me = PersonRepo(request=request).me
        image = ImageRepo(request=request).image(*args, **kwargs)
        if image is None:
            raise Http404
        context=getContext(request=request)
        context['image']=image
        context[NO_FOOTER]=True
        context[NO_NAVBAR]=True
        context[WIDE_LAYOUT]=True 
        return render(request,TEMPLATE_ROOT+"image.html",context)
         
       
class ImageDownloadView(View):
    def get(self, request, *args, **kwargs): 
        image = ImageRepo(request=request).image(*args, **kwargs)
        if image is None:
            raise Http404
        return image.download_response()



class LocationView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        location = LocationRepo(request=request).location(*args, **kwargs)
        context['location'] = location
        context['location_s'] = json.dumps(LocationSerializer(location).data)

        return render(request, TEMPLATE_ROOT+"location.html", context)
  

class AreaView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        area = AreaRepo(request=request).area(*args, **kwargs)
        context['area'] = area
        for installed_app in context['installed_apps']:
            if installed_app['name']=='market':
                from market.repo import SupplierRepo,CustomerRepo
                from market.serializers import SupplierSerializer,CustomerSerializer
              
                suppliers=SupplierRepo(request=request).list(region_id=area.id)
                context['suppliers'] = suppliers
                suppliers_s=json.dumps(SupplierSerializer(suppliers,many=True).data)
                context['suppliers_s']=suppliers_s

                
                customers=CustomerRepo(request=request).list(region_id=area.id)
                context['customers'] = customers
                customers_s=json.dumps(CustomerSerializer(customers,many=True).data)
                context['customers_s']=customers_s
        context['area_s'] = json.dumps(AreaSerializer(area).data)
        return render(request, TEMPLATE_ROOT+"area.html", context)


class AreasView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        areas = AreaRepo(request=request).list(*args, **kwargs)
        context['areas'] = areas
        context['areas_s'] = json.dumps(AreaSerializer(areas,many=True).data)
        if request.user.has_perm(APP_NAME+".add_area"):
            context['add_area_form']=AddAreaForm()
            context['colors']=(color[0] for color in ColorEnum.choices)
        return render(request, TEMPLATE_ROOT+"areas.html", context)


class LocationsView(View):  
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        locations = LocationRepo(request=request).list(*args, **kwargs)
        context['locations'] = locations
        context['locations_s'] = json.dumps(LocationSerializer(locations,many=True).data)
        if request.user.has_perm(APP_NAME+".add_location"):
            context['add_location_form']=AddLocationForm()
        return render(request, TEMPLATE_ROOT+"locations.html", context)