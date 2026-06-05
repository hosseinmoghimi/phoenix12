from django.shortcuts import render
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL,CURRENCY,VUE_VERSION_3,VUE_VERSION_2,CURRENCY_TUMAN
from phoenix.settings import VERSION
from authentication.views import PersonRepo,PersonSerializer
from utility.repo import ParameterRepo,PictureRepo
from django.views import View
from .enums import *
from .forms import *
from .repo import PageRepo,EventRepo
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from utility.log import leolog
from utility.views import MessageView
from django.utils import timezone
import json
from .repo import PageRepo,FAILED,SUCCEED
from .serializers import PageSerializer,PageBriefSerializer,EventSerializer
from utility.enums import ColorEnum
from utility.constants import *
LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='core/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR"
def CoreContext(request,*args, **kwargs):
    context={}
    app_name='core'
    if 'app_name' in kwargs:
        app_name=kwargs['app_name']
    context['APP_NAME']=app_name
    context['VUE_VERSION_3']=VUE_VERSION_3
    context['VUE_VERSION_2']=VUE_VERSION_2
    context['DEBUG']=DEBUG



    if 'NO_APP_NAVBAR' in kwargs and not kwargs['NO_APP_NAVBAR']:
        pass 
    else:
        context['APP_NAVBAR']=app_name+'/includes/navbar.html'

    if 'NO_APP_SCRIPT' in kwargs and not kwargs['NO_APP_SCRIPT']:
        pass 
    else:
        context['APP_SCRIPT']=app_name+'/includes/script.html'
    if 'NO_APP_FOOTER' in kwargs and not kwargs['NO_APP_FOOTER']:
        pass 
    else:
        context['APP_FOOTER']=app_name+'/includes/footer.html'



    me_person=PersonRepo(request=request).me

    if me_person is not None:
        from django.contrib.auth.models import Group
        price_group = Group.objects.get_or_create(name = PRICE_GROUP_NAME)
        quantity_group = Group.objects.get_or_create(name = QUANTITY_GROUP_NAME)
        balance_group = Group.objects.get_or_create(name = BALANCE_GROUP_NAME)
        SHOW_PRICE=False
        SHOW_QUANTITY=False
        SHOW_BALANCE=False
        if me_person is not None and me_person.user is not None:
            price_group=me_person.user.groups.filter(name=PRICE_GROUP_NAME).first()
            quantity_group=me_person.user.groups.filter(name=QUANTITY_GROUP_NAME).first()
            balance_group=me_person.user.groups.filter(name=BALANCE_GROUP_NAME).first()
            if quantity_group is not None:
                SHOW_QUANTITY=True 
            if balance_group is not None:
                SHOW_BALANCE=True 
            if price_group is not None:
                SHOW_PRICE=True
        context['SHOW_QUANTITY']=SHOW_QUANTITY
        context['SHOW_BALANCE']=SHOW_BALANCE
        context['SHOW_PRICE']=SHOW_PRICE
        context['me_person']=me_person 
        me_person_s=json.dumps(PersonSerializer(me_person).data)
        context['me_person_s']=me_person_s 
        from authentication.views import ClipBoardItemContext,MyLinksContext
        context.update(ClipBoardItemContext(request=request,person=me_person))
        context.update(MyLinksContext(request=request,person=me_person))
    context['ADMIN_URL']=ADMIN_URL
    context['STATIC_URL']=STATIC_URL
    context['SITE_URL']=SITE_URL
    context['CURRENCY']=CURRENCY
    context['CURRENCY_TUMAN']=CURRENCY_TUMAN
    persian_date=PersianCalendar() 
    now=timezone.now()
    current_datetime=persian_date.from_gregorian(now) 
    current_date=current_datetime[0:10]

    context['current_datetime']=current_datetime
    context['current_date']=current_date
    current_time=current_datetime[10:]
    context['current_time']=current_time

    context['VERSION']=VERSION
    context['phoenix_apps']=phoenix_apps
    if me_person is not None:
        context['me_person']=me_person
    parameter_repo=ParameterRepo(request=request,app_name=app_name)
    context['WIDE_LAYOUT']=parameter_repo.parameter(name=PARAMETER_NAME_ENUM.WIDE_LAYOUT,default="0").boolean_value
    context['farsi_font_name']=parameter_repo.parameter(name=PARAMETER_NAME_ENUM.FARSI_FONT,default="Shabnam").value
    parameter_repo.set_parameter(app_name=APP_NAME,name="version",value=VERSION)
     
    # app_background_image=PictureRepo(request=request,app_name=app_name).picture(name=PictureNameEnum.APP_BACKGROUND_IMAGE)
    # if app_has_background:
    #     context['app_background_image']=app_background_image

    for appp in phoenix_apps:
        if appp['name']==app_name:
            # context['current_app']={'name':appp['name'],'title':appp['title'],'url':appp['url'],'logo':appp['logo']}
            context['current_app']=appp
            context['app_title']=appp['title']
    from messenger.views import MessengerContext
    context.update(MessengerContext(request=request,me_person=me_person))
    return context

        
def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
    if 'me_person' in context:
        me_person=context['me_person']
        if me_person is not None:
             
            from attachments.repo import LikeRepo
            my_likes=LikeRepo(request=request).list(person_id=me_person.id)
            ids=[]
            for like in my_likes:
                ids.append(like.page.id)
            pages=PageRepo(request=request).list(ids=ids)
            if pages is not None and len(pages)>0:
                pages_s=json.dumps(PageBriefSerializer(pages,many=True).data)
                context['pages_s']=pages_s
                context['pages']=pages
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

def PageContext(request,page,*args, **kwargs):
    context={}
    context['page']=page
    context['title']=page.title
    page_s=json.dumps(PageSerializer(page).data)
    context['page_s']=page_s
    me_person=PersonRepo(request=request).me
    from attachments.views import PageTagsContext,PageLocationsContext,PageImagesContext,PageRelatedContext,PagPrintsContext,PageLikesContext,PageCommentsContext,PageLinksContext,PageDownloadsContext
    if request.user.has_perm(APP_NAME+'.change_page'):
        colors=(i[0] for i in ColorEnum.choices)
        context['colors_for_page_thumbnail_app']=colors
        context['set_page_thumbnail_header_form']=SetPageThumbnailHeaderForm()
    context.update(PageLikesContext(request=request,page=page,person=me_person))
    context.update(PageCommentsContext(request=request,page=page,person=me_person))
    context.update(PageLinksContext(request=request,page=page,person=me_person))
    context.update(PageDownloadsContext(request=request,page=page,person=me_person))
    context.update(PageImagesContext(request=request,page=page,person=me_person))
    context.update(PageRelatedContext(request=request,page=page,person=me_person))
    context.update(PageLocationsContext(request=request,page=page,person=me_person))
    context.update(PageTagsContext(request=request,page=page,person=me_person))
    context.update(PagPrintsContext(request=request,page=page,person=me_person))
    return context

def SearchContext(request,search_for,*args, **kwargs):
    context={}
    WAS_FOUND=False
    pages=PageRepo(request=request).list(search_for=search_for)
    if len(pages)>0:
        context['pages']=pages
        context['pages_s']=json.dumps(PageBriefSerializer(pages,many=True).data)
        WAS_FOUND=True

    if WAS_FOUND:
               context['WAS_FOUND']=WAS_FOUND
    return context

class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps 
         
        return render(request,TEMPLATE_ROOT+"search.html",context)

    def post(self,request,*args, **kwargs):
        result=FAILED
        search_for=''
        message=''
        log=1
        context=getContext(request=request) 
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            log=2
            search_for=search_form.cleaned_data['search_for']
            app_name=search_form.cleaned_data['app_name']
            result=SUCCEED
            WAS_FOUND=False
            SEARCH_IN_ALL_APPS=False

            if app_name=='accounting' or SEARCH_IN_ALL_APPS:
                from accounting.views import SearchContext as accounting_SearchContext
                context.update(accounting_SearchContext(request=request,search_for=search_for))
                if context['WAS_FOUND']:
                    WAS_FOUND=True


            if app_name=='core' or SEARCH_IN_ALL_APPS:
                from core.views import SearchContext as core_SearchContext
                context.update(core_SearchContext(request=request,search_for=search_for))
                if context['WAS_FOUND']:
                    WAS_FOUND=True


            if app_name=='projectmanager' or SEARCH_IN_ALL_APPS:
                from projectmanager.views import SearchContext as projectmanager_SearchContext
                context.update(projectmanager_SearchContext(request=request,search_for=search_for))
                if context['WAS_FOUND']:
                    WAS_FOUND=True


            if app_name=='warehouse' or SEARCH_IN_ALL_APPS:
                from warehouse.views import SearchContext as warehouse_SearchContext
                context.update(warehouse_SearchContext(request=request,search_for=search_for))
                if context['WAS_FOUND']:
                    WAS_FOUND=True


            if app_name=='authentication' or SEARCH_IN_ALL_APPS:
                from authentication.views import SearchContext as authentication_SearchContext
                context.update(authentication_SearchContext(request=request,search_for=search_for))
                if context['WAS_FOUND']:
                    WAS_FOUND=True

            
            if app_name=='attachments' or SEARCH_IN_ALL_APPS:
                from attachments.views import SearchContext as attachments_SearchContext
                context.update(attachments_SearchContext(request=request,search_for=search_for))
                if context['WAS_FOUND']:
                    WAS_FOUND=True
            
            if app_name=='market' or SEARCH_IN_ALL_APPS:
                from market.views import SearchContext as market_SearchContext
                context.update(market_SearchContext(request=request,search_for=search_for))
                if context['WAS_FOUND']:
                    WAS_FOUND=True
            
            if app_name=='organization' or SEARCH_IN_ALL_APPS:
                from organization.views import SearchContext as organization_SearchContext
                context.update(organization_SearchContext(request=request,search_for=search_for))
                if context['WAS_FOUND']:
                    WAS_FOUND=True
        
            
            
             
        context['message']=message
        context['search_for']=search_for
        context['log']=log
        context['result']=result
        if WAS_FOUND:
               context['WAS_FOUND']=WAS_FOUND
        return render(request, "utility/search.html",context)

class PageView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        page=PageRepo(request=request).page(*args, **kwargs)
        if page is None:
            mv=MessageView()
            return mv.get(request=request)
        context.update(PageContext(request=request,page=page))
        return render(request,TEMPLATE_ROOT+"page.html",context)
 
class EventView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        event=EventRepo(request=request).event(*args, **kwargs)
        if event is None:
            mv=MessageView()
            return mv.get(request=request)
        context.update(PageContext(request=request,page=event))
        return render(request,TEMPLATE_ROOT+"event.html",context)
 
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)
 
class ComingSoonView(View):
    def get(self,request,*args, **kwargs):
        context={}
        context['name3']="name 3333"
        context['NOT_FOOTER']=True
        context['NOT_NAVBAR']=True
        context['WIDE_LAYOUT']=True
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        coming_soon_title=parameter_repo.parameter(name="عنوان بزودی").value
        coming_soon_subtitle=parameter_repo.parameter(name="زیرعنوان بزودی").value
        coming_soon_page_title=parameter_repo.parameter(name="عنوان صفحه بزودی").value
        coming_soon_text=parameter_repo.parameter(name="متن بزودی").value
        context['coming_soon_title']=coming_soon_title
        context['coming_soon_subtitle']=coming_soon_subtitle
        context['coming_soon_text']=coming_soon_text
        context['coming_soon_page_title']=coming_soon_page_title
        coming_soon_picture=PictureRepo(request=request,app_name=APP_NAME).picture(name='coming_soon')
        context['coming_soon_picture']=coming_soon_picture
        context['LAYOUT_PARENT']=LAYOUT_PARENT
        return render(request,"comingsoon/index.html",context)
 