from .models import Person,FAILED,SUCCEED,APP_NAME,ClipBoardItem,MyLink
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from utility.log import leolog

 
class PersonRepo():
    def user(self,*args, **kwargs):
        user_id=0
        self.objects=Person.objects.filter(pk=0)
        if 'user_id' in kwargs:
            user_id=kwargs['user_id']
            return User.objects.filter(pk=user_id).first()
        return User.objects.filter(pk=0).first()
    def __init__(self,request,*args, **kwargs):
        self.me=None
        self.request=request
        if request.user.is_authenticated:
            self.me=Person.objects.filter(user_id=request.user.id).first()
            if self.request.user.has_perm(APP_NAME+'.view_person'):
                self.objects=Person.objects.all()
            else:
                self.objects=Person.objects.filter(user_id=request.user.id)  
    def list(self,*args, **kwargs):
        objects=self.objects
        from django.db.models import Q
        if "search_for" in kwargs:
            search_for=kwargs["search_for"]
            objects=objects.filter(Q(full_name__contains=search_for)  | Q(melli_code__contains=search_for) )
        return objects.all()
    def change_image(self,person_id,image):
        person=self.person(person_id=person_id)
        if person is not None:
            person.image_origin = image
            person.save()
            return SUCCEED
        return FAILED
    
    def person(self,*args, **kwargs):
        if "person_id" in kwargs and kwargs["person_id"] is not None:
            return self.objects.filter(pk=kwargs['person_id']).first()
        if "person" in kwargs:
            return kwargs['person'] 
        if "melli_code" in kwargs and kwargs['melli_code'] is not None and not kwargs['melli_code']=="":
            return self.objects.filter(melli_code=kwargs['melli_code']).first() 
        if "pk" in kwargs and kwargs["pk"] is not None:
            return self.objects.filter(pk=kwargs['pk']).first() 
        if "id" in kwargs and kwargs["id"] is not None:
            return self.objects.filter(pk=kwargs['id']).first() 
        if "code" in kwargs and kwargs["code"] is not None:
            return self.objects.filter(code=kwargs['code']).first()
             
        if "account_code" in kwargs and kwargs["account_code"] is not None:
            a= self.objects.filter(code=kwargs['account_code']).first() 
            if a is not None:
                return a
            else:
                try:
                    a= self.objects.filter(pure_code=filter_number(kwargs['account_code'])).first() 
                    if a is not None:
                        return a
                except:
                    pass
    def change_password(self,request,*args, **kwargs):
        result,message=FAILED,'خطا'
        if self.request.user.has_perm(APP_NAME+".change_person"):
            user=User.objects.filter(username=kwargs['username']).first()
        else:
            user=authenticate(request=request,username=kwargs['username'],password=kwargs['old_password'])
            if user is None:
                message='نام کاربری و کلمه عبور صحیح نمی باشد.'
                return (request,user,result,message)
        if user is not None:
            user.set_password(kwargs['new_password'])
            user.save()
            login(request,user)
            if user.is_authenticated:
                result=SUCCEED
                message='با موفقیت تغییر یافت.'
            return (request,user,result,message)

    

    def delete_all(self,*args,**kwargs):
        result,message=FAILED,''
        if not self.request.user.has_perm(APP_NAME+".delete_person"):
            message="دسترسی غیر مجاز"
            return result,message
        # PersonCategory.objects.all().delete()
        Person.objects.all().delete()
        result=SUCCEED
        message="همه اشخاص حذف شدند."
        return result,message
    
    def add_person(self,*args,**kwargs):
        result,message,person=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".add_person"):
            message="دسترسی غیر مجاز"
            return result,message,person

        person=Person()
        person_category_id=0
        categories=[]
        person_account_categories=[]

        # if 'person_id' in kwargs:
        #     if Person.objects.filter(person_id=kwargs['person_id']).first() is not None:
        #         message="کد پروفایل وارد شده تکراری است."
        #         person=None
        #         return result,message,person
        if 'melli_code' in kwargs:
            melli_code=kwargs['melli_code']

            if melli_code is not None and len(melli_code)>0 and Person.objects.filter(melli_code=melli_code).first() is not None:
                message="کد ملی وارد شده تکراری است."
                person=None
                return result,message,person
            
        

        if 'birth_date' in kwargs:
            person.birth_date=kwargs["birth_date"]
        if 'birth_location' in kwargs:
            person.birth_location=kwargs["birth_location"]

  
        if 'type2' in kwargs:
            person.type2=kwargs["type2"]
        if 'type' in kwargs:
            person.type=kwargs["type"]
        if 'melli_code' in kwargs:
            person.melli_code=kwargs["melli_code"]
        if 'title' in kwargs:
            person.title=kwargs["title"]

        if 'postal_code' in kwargs:
            person.postal_code=kwargs["postal_code"]
        if 'melli_code' in kwargs:
            person.melli_code=kwargs["melli_code"]
        if 'economic_no' in kwargs:
            person.economic_no=kwargs["economic_no"]
        if 'tel' in kwargs:
            person.tel=kwargs["tel"]
            
 


        if 'user_id' in kwargs :
            user_id=kwargs['user_id']
            if user_id is not None and user_id>0:
                if len(Person.objects.filter(user_id=user_id))>0:
                    message='این یوزر قبلا به شخصی واگذار شده است.'
                    return FAILED,message,None
                person.user_id=user_id
        if 'color' in kwargs:
            person.color=kwargs["color"]
        if 'first_name' in kwargs:
            person.first_name=kwargs["first_name"]
        if 'last_name' in kwargs:
            person.last_name=kwargs["last_name"]
        if 'bio' in kwargs:
            person.bio=kwargs["bio"]
        if 'email' in kwargs:
            person.email=kwargs["email"]
        if 'mobile' in kwargs:
            person.mobile=kwargs["mobile"]
        if 'father_name' in kwargs:
            person.father_name=kwargs["father_name"]
        if 'prefix' in kwargs:
            person.prefix=kwargs["prefix"]
        if 'gender' in kwargs:
            person.gender=kwargs["gender"]
        if 'address' in kwargs:
            person.address=kwargs["address"]  
        if 'type' in kwargs:
            person.type=kwargs["type"] 
         
          
        (result,message,person)=person.save()
        if result==FAILED:
            return result,message,person
        

 
        return result,message,person


    def edit_person(self,*args,**kwargs):
        result,message,person=FAILED,"",None
        person=Person.objects.filter(id=kwargs['person_id']).first()
        if person is None:
            message='چنین شخصی پیدا نشد.'
            return FAILED,message,None
        
        if self.me is None:
            if not person.id==self.me.id:
                if not self.request.user.has_perm(APP_NAME+".add_person"):
                    message="دسترسی غیر مجاز"
                    return result,message,person
 
        # if 'person_id' in kwargs:
        #     if Person.objects.filter(person_id=kwargs['person_id']).first() is not None:
        #         message="کد پروفایل وارد شده تکراری است."
        #         person=None
        #         return result,message,person
        if 'melli_code' in kwargs:
            melli_code=kwargs['melli_code']

            if melli_code is not None and len(melli_code)>0 and Person.objects.exclude(id=person.id).filter(melli_code=melli_code).first() is not None:
                message="کد ملی وارد شده تکراری است."
                person=None
                return result,message,person
            
        
        if 'father_name' in kwargs:
            person.father_name=kwargs["father_name"]

        if 'birth_date' in kwargs:
            person.birth_date=kwargs["birth_date"]
        if 'birth_location' in kwargs:
            person.birth_location=kwargs["birth_location"]

  
        if 'type2' in kwargs:
            person.type2=kwargs["type2"]
        if 'type' in kwargs:
            person.type=kwargs["type"]
        if 'melli_code' in kwargs:
            person.melli_code=kwargs["melli_code"]
        if 'title' in kwargs:
            person.title=kwargs["title"]

        if 'postal_code' in kwargs:
            person.postal_code=kwargs["postal_code"]
        if 'melli_code' in kwargs:
            person.melli_code=kwargs["melli_code"]
        if 'economic_no' in kwargs:
            person.economic_no=kwargs["economic_no"]
        if 'tel' in kwargs:
            person.tel=kwargs["tel"]
             

 
        if 'color' in kwargs:
            person.color=kwargs["color"]
        if 'first_name' in kwargs:
            person.first_name=kwargs["first_name"]
        if 'last_name' in kwargs:
            person.last_name=kwargs["last_name"]
        if 'bio' in kwargs:
            person.bio=kwargs["bio"]
        if 'email' in kwargs:
            person.email=kwargs["email"]
        if 'mobile' in kwargs:
            person.mobile=kwargs["mobile"]
        if 'prefix' in kwargs:
            person.prefix=kwargs["prefix"]
        if 'gender' in kwargs:
            person.gender=kwargs["gender"]
        if 'address' in kwargs:
            person.address=kwargs["address"]  
        if 'type' in kwargs:
            person.type=kwargs["type"] 
         
          
        (result,message,person)=person.save()
        if result==FAILED:
            return result,message,person
        

 
        return result,message,person


    def logout(self,*args, **kwargs):
        if 'request' in kwargs:
            logout(request=kwargs['request'])
        else:
            logout(request=self.request)
    def login(self,*args, **kwargs):
        request=self.request
        from log.repo import LogRepo
        logout(request=request)
        if 'user' in kwargs:
            user=kwargs['user']
            if user is not None:
                login(request,user)
                if user.is_authenticated:
                    person=Person.objects.filter(user=user).first()
                    description='لاگین با موفقیت انجام شد.'
                    title='لاگین'
                    url=person.get_absolute_url()
                    LogRepo(request=self.request).add_log(title=title,url=url,person=person,app_name=APP_NAME,description=description)
                   

                    return (request,user)
        if 'username' in kwargs and 'password' in kwargs:
            user=authenticate(request=request,username=kwargs['username'],password=kwargs['password'])
            if user is not None:
                login(request,user)
                if user.is_authenticated:
                    person=Person.objects.filter(user=user).first()
                    description='لاگین با موفقیت انجام شد.'
                    title='لاگین'
                    url=person.get_absolute_url()
                    LogRepo(request=self.request).add_log(title=title,url=url,person=person,app_name=APP_NAME,description=description)
                    return (request,user)
        LogRepo(request=self.request).add_log(title="try to login",url=url,app_name=APP_NAME,description="try to login username:"+kwargs['username']+" , password : "+kwargs['password'])
    
 
class ClipBoardItemRepo():
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user 
        self.me_person=PersonRepo(request=self.request).me
        self.objects=ClipBoardItem.objects.filter(person=self.me_person)
    def clear_all_clipboard_items(self,*args, **kwargs):
        clip_board_items=ClipBoardItem.objects.filter(person_id=self.me_person.id)
        clip_board_items.delete()
        return SUCCEED


    def list(self,*args, **kwargs):
        return self.objects.all()
     
    def add_clipboard_item(self,*args,**kwargs):

        result=FAILED
        if self.me_person is None:
            return FAILED
        clip_board_item=ClipBoardItem(person_id=self.me_person.id,*args,**kwargs)
        old=ClipBoardItem.objects.filter(person_id=clip_board_item.person.id).filter(name=clip_board_item.name).filter(text=clip_board_item.text).first()
        if old is not None:
            old.delete()
        clip_board_item.save()

        clip_board_item_list=ClipBoardItem.objects.filter(person_id=self.me_person)
        from utility.repo import ParameterRepo
        parameter_repo=ParameterRepo(request=self.request,app_name=APP_NAME)
        CLIPBODRD_MAX_LENGTH=parameter_repo.parameter(name="حداکثر تعداد کلیپ بورد ها ",default=5).int_value
        if len(clip_board_item_list)>CLIPBODRD_MAX_LENGTH :
            clip_board_item_list.first().delete()
        result=SUCCEED
        return result




class MyLinkRepo:
    
    def __init__(self,*args, **kwargs):
        self.app_name=""
        self.request=None
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user 
        self.me_person=PersonRepo(request=self.request).me
        self.objects=MyLink.objects.filter(person=self.me_person).order_by('priority')


    def list(self,*args, **kwargs):
        return self.objects.all()
    def delete_my_link(self,my_link_id):
        result,my_links=FAILED,[]
        my_link=MyLink.objects.filter(person_id=self.me_person.id).filter(id=my_link_id).first()
        if my_link is not None:
            my_link.delete()
            result=SUCCEED
            my_links= MyLink.objects.filter(person_id=self.me_person.id).order_by('link__priority')
        return result,my_links
    def add_my_link(self,*args,**kwargs):
        result=FAILED
        if self.me_person is None:
            return FAILED
        from attachments.models import Link
        my_link=MyLink(person_id=self.me_person.id)
        if 'title' in kwargs:
            my_link.title=kwargs['title']
        if 'url' in kwargs:
            my_link.url=kwargs['url']
        if 'priority' in kwargs:
            my_link.priority=kwargs['priority']
        my_link.person_id=self.me_person.id
        my_link.save()

        my_link_list=MyLink.objects.filter(person_id=self.me_person).order_by('priority')
        MY_LINKS_LENGTH=0
        from utility.repo import ParameterRepo
        MY_LINKS_LENGTH=ParameterRepo(request=self.request,app_name=APP_NAME).parameter(name='MY_LINKS_LENGTH',default=5).int_value
        if len(my_link_list)>MY_LINKS_LENGTH :
            my_link_list.first().delete()
        result=SUCCEED
        return result
