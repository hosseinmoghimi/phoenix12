from django.shortcuts import render,redirect,reverse
from phoenix.server_settings import DEBUG,ADMIN_URL,MEDIA_URL,SITE_URL,STATIC_URL,ONLY_HTTPS
from django.views import View
from .serializers import PersonSerializer,PersonFullSerializer,MyLinkSerializer,ClipBoardItemSerializer
from .repo import PersonRepo,FAILED,SUCCEED
from .forms import *
from django.http import HttpResponseRedirect
from .apps import APP_NAME
from phoenix.server_apps import phoenix_apps
from utility.calendar import PersianCalendar
from core.views import MessageView,CoreContext,ParameterRepo,PictureRepo,leolog
import json

LAYOUT_PARENT='phoenix/layout.html'
TEMPLATE_ROOT='authentication/'
WIDE_LAYOUT="WIDE_LAYOUT"
NO_FOOTER="NO_FOOTER"
NO_NAVBAR="NO_NAVBAR" 

def getContext(request,*args, **kwargs):
    context=CoreContext(app_name=APP_NAME,request=request)
  
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context
 


 
def ClipBoardItemContext(request,*args, **kwargs):
    context={}
    if 'person' in kwargs:
        person=kwargs['person']
    if person is None:
        from authentication.repo import PersonRepo
        person=PersonRepo(request=request).me
    if person is None:
        return {}
    from .repo import ClipBoardItemRepo
    clipboard_items=ClipBoardItemRepo(request=request).list().order_by('id')
    if len(clipboard_items)>0:
        context['clipboard_items']=clipboard_items
    return context


def MyLinksContext(request,*args, **kwargs):
    context={}
    if 'person' in kwargs:
        person=kwargs['person']
    if person is None:
        from authentication.repo import PersonRepo
        person=PersonRepo(request=request).me
    if person is None:
        return {}
    from .repo import MyLinkRepo
    my_links=MyLinkRepo(request=request).list()
    if len(my_links)>0:
        context['my_links']=my_links
        my_links_s=json.dumps(MyLinkSerializer(my_links,many=True).data)
        context['my_links_s']=my_links_s
    return context



def AddPersonContext(request,*args, **kwargs):
    context={}
    from .enums import PersonType2Enum,PersonTypeEnum
    from utility.enums import PersonPrefixEnum,GenderEnum
    context['prefixes']=(i[0] for i in PersonPrefixEnum.choices)
    context['genders']=(i[0] for i in GenderEnum.choices)
    context['types']=(i[0] for i in PersonTypeEnum.choices)
    context['types2']=(i[0] for i in PersonType2Enum.choices)
    from django.contrib.auth.models import User
    users_for_add_person_app=User.objects.filter(pk__gt=0)
    context['users_for_add_person_app']=users_for_add_person_app

    return context


def PersonContext(request,*args, **kwargs):
    context={}
    person=PersonRepo(request=request).person(*args, **kwargs)
    if request.user.has_perm('authentication.change_person'):
        if person.user is not None: 
            context['login_as_form']=True 
    context['person']=person
    person_s=json.dumps(PersonSerializer(person).data)
    context['person_s']=person_s

    from core.views import PageBriefSerializer,PageRepo
    from attachments.repo import LikeRepo
    my_likes=LikeRepo(request=request).list(person_id=person.id)
    ids=[]
    for like in my_likes:
        ids.append(like.page.id)
    pages=PageRepo(request=request).list(ids=ids)
    if pages is not None and len(pages)>0:
        pages_s=json.dumps(PageBriefSerializer(pages,many=True).data)
        context['pages_s']=pages_s
        context['pages']=pages
    return context
     

def SearchContext(request,search_for,*args, **kwargs):
    context={}
    WAS_FOUND=False
    

    persons=PersonRepo(request=request).list(search_for=search_for)
    if len(persons)>0:
        context['persons']=persons
        context['persons_s']=json.dumps(PersonSerializer(persons,many=True).data)
        WAS_FOUND=True


    if WAS_FOUND:
               context['WAS_FOUND']=WAS_FOUND
    return context


class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        phoenix_apps=context["phoenix_apps"]
        phoenix_apps=phoenix_apps
        phoenix_apps = sorted(phoenix_apps, key=lambda d: d['priority'])

        context['phoenix_apps']=phoenix_apps
        return render(request,TEMPLATE_ROOT+"index.html",context)

 

class ChangePersonImageView(View):
    def post(self,request,*args, **kwargs):
        person_id=0
        if 'pk' in kwargs:
            person_id=kwargs['pk']
        log=1 
        change_person_image_form=ChangePersonImageForm(request.POST,request.FILES)
        if change_person_image_form.is_valid():
            log=3          
            person_id=change_person_image_form.cleaned_data['person_id']
            image=request.FILES['image']
            result=PersonRepo(request=request).change_image(person_id=person_id,
            image=image,
            )
        return redirect(reverse(APP_NAME+":person",kwargs={'pk':person_id}))


class LoginAsViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        if request.user.has_perm(APP_NAME+".change_person"):
            selected_person=PersonRepo(request=request).person(*args, **kwargs)
            if selected_person is not None:
                PersonRepo(request=request).login(request=request,user=selected_person.user)
                return redirect('core:index')
        return redirect(APP_NAME+":login")


class PersonsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['name3']="name 3333"
        persons=PersonRepo(request=request).list(*args, **kwargs).order_by('full_name')
        persons_s=json.dumps(PersonSerializer(persons,many=True).data)
        context['persons']=persons
        context['persons_s']=persons_s
        if request.user.has_perm(APP_NAME+'.add_person'):
            context['add_person_form']=AddPersonForm()
            context.update(AddPersonContext(request=request))
        return render(request,TEMPLATE_ROOT+"persons.html",context)


class PersonView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        person=PersonRepo(request=request).person(*args, **kwargs)
        if person is None:
            title='شخص پیدا نشد.'
            body='شخص پیدا نشد.'
            mv=MessageView(title=title,body=body)
            return mv.get(request=request)
        context.update(PersonContext(request=request,person=person))
        context['person']=person
        person_s=json.dumps(PersonFullSerializer(person).data)
        context['person_s']=person_s
        context['title']=person.full_name
        me_person=PersonRepo(request=request).me
        if me_person is not None:
            if request.user.has_perm(APP_NAME+'.change_person') or person.user==me_person.user:
                context['change_person_image_form']=ChangePersonImageForm()
                context['edit_person_form']=EditPersonForm()
                from .enums import PersonType2Enum,PersonTypeEnum
                from utility.enums import PersonPrefixEnum,GenderEnum
                context['prefixes_for_edit_person_app']=(i[0] for i in PersonPrefixEnum.choices)
                context['genders_for_edit_person_app']=(i[0] for i in GenderEnum.choices)
                context['types_for_edit_person_app']=(i[0] for i in PersonTypeEnum.choices)
                context['types2_for_edit_person_app']=(i[0] for i in PersonType2Enum.choices)

        return render(request,TEMPLATE_ROOT+"person.html",context)
    
class RegisterView(View):
    def get(self,request,*args, **kwargs): 
        messages=[]
        if 'messages' in kwargs:
            messages=kwargs['messages']
        context=getContext(request=request)
        context['register_form_header_image']=PictureRepo(request=request,app_name=APP_NAME).picture(name="تصویر ثبت نام")
        context['messages']=messages
        

        PersonRepo(request=request).logout(request)
        context['register_form']=RegisterForm() 
         
        return render(request,TEMPLATE_ROOT+"register.html",context)
     
    def post(self,request,*args, **kwargs):
        next=SITE_URL

        messages=[]
        login_form=LoginForm(request.POST)
        next=request.POST['next']
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            if 'next' in login_form.cleaned_data:
                next=login_form.cleaned_data['next']
            
            a=PersonRepo(request=request).login(request=request,username=username,password=password)
            if a is not None:
                (request,user)=a
                return HttpResponseRedirect(next)
            messages.append("نام کاربری و کلمه عبور صحیح نمی باشد.")
        return self.get(request=request,messages=messages)
            

 
 
class LoginView(View):
    def get(self,request,*args, **kwargs): 
        messages=[]
        if 'messages' in kwargs:
            messages=kwargs['messages']
        context=getContext(request=request)
        context['login_form_header_image']=PictureRepo(request=request,app_name=APP_NAME).picture(name="تصویر لاگین")
        context['messages']=messages
        if 'next' in request.GET:
            context['next']=request.GET['next']
        else:
            context['next']=SITE_URL

        PersonRepo(request=request).logout(request)
        context['login_form']=LoginForm()
        context['build_absolute_uri']=request.build_absolute_uri()
        build_absolute_uri=request.build_absolute_uri()
        if ONLY_HTTPS and "http://" in build_absolute_uri :
            build_absolute_uri=build_absolute_uri.replace("http:","https:")
            return redirect(build_absolute_uri)
        return render(request,TEMPLATE_ROOT+"login.html",context)
     
    def post(self,request,*args, **kwargs):
        next=SITE_URL

        messages=[]
        login_form=LoginForm(request.POST)
        next=request.POST['next']
        if login_form.is_valid():
            username=login_form.cleaned_data['username']
            password=login_form.cleaned_data['password']
            if 'next' in login_form.cleaned_data:
                next=login_form.cleaned_data['next']
            
            a=PersonRepo(request=request).login(request=request,username=username,password=password)
            if a is not None:
                (request,user)=a
                return HttpResponseRedirect(next)
            messages.append("نام کاربری و کلمه عبور صحیح نمی باشد.")
        return self.get(request=request,messages=messages)
            

class ChangePasswordView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request) 
        person_repo=PersonRepo(request=request)
        person=person_repo.person(*args, **kwargs)
        if person is None:
            person=PersonRepo(request=request).me
        if person is not None and person.user is not None:
            context['username']=person.user.username
        context['NOT_NAVBAR']=True
        context['NOT_FOOTER']=True
        return render(request,TEMPLATE_ROOT+"change-password.html",context)
    def post(self,request,*args, **kwargs):
        from .apis import ChangePasswordApi
        return ChangePasswordApi().post(request,*args, **kwargs)

class LogoutView(View):
    def get(self,request,*args, **kwargs):
        PersonRepo(request=request).logout(request)
        message='شما با موفقیت از سیستم خارج شدید.'
        return LoginView().get(request=request,messages=[message])
