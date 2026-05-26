from core.repo import PageRepo,PersonRepo,FAILED,SUCCEED
from .models import Like,Comment,Link,Download,Image,Location,Area, Tag,PagePrint
from .apps import APP_NAME
from django.db.models import Q
from .enums import PagePrintTypeEnum
from utility.log import leolog


class ImageRepo():

    def __init__(self,request,*args, **kwargs):
        self.objects=Image.objects
        self.request=request
    def list(self,*args, **kwargs):
        objects=Image.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(Q(title__contains=kwargs['search_for']))
        return objects.all()
    def image(self,*args, **kwargs):
        if 'pk' in kwargs and kwargs['pk'] is not None:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs and kwargs['id'] is not None:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'image_id' in kwargs and kwargs['image_id'] is not None:
            return self.objects.filter(pk=kwargs['image_id']).first()
    def add_image(self,*args, **kwargs):
        result,message,image=FAILED,"",None
        title=''
        if not self.request.user.has_perm(APP_NAME+'.add_image'):
            message='دسترسی غیر مجاز'
            return FAILED,message,None
        me_person=PersonRepo(request=self.request).me
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if me_person is None:
            return None
        if page is None:
            return None
        if 'title' in kwargs:
            title=kwargs['title']

        if 'image' in kwargs:
            image_text=kwargs['image']
        if image_text is None:
            return result,message,image
        image=Image(creator_id=me_person.id,page_id=page.id,image_main_origin=image_text,title=title)
        image.save()
        result=SUCCEED
        message='تصویر با موفقیت اضافه شد.'
        return result,message,image
    
    def delete_image(self,*args, **kwargs):
        me_person=PersonRepo(request=self.request).me
        if 'image_id' in kwargs:
            image_id=kwargs['image_id']
        # images=Image.objects.filter(person_id=me_person.id).filter(pk=image_id)
        images=Image.objects.filter(pk=image_id)
        images.delete()
        result=SUCCEED
        message="کامنت با موفقیت حذف گردید."
        return result,message


   
class PagePrintRepo():

    def __init__(self,request,*args, **kwargs):
        self.objects=PagePrint.objects
        self.request=request
    def list(self,*args, **kwargs):
        objects=PagePrint.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        if 'person_id' in kwargs:
            objects=objects.filter(person_id=kwargs['person_id'])
        return objects.all()

    def add_page_print(self,*args, **kwargs):
        result,message,page_print=FAILED,"",None
        me_person=PersonRepo(request=self.request).me
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if me_person is None:
            return result,message,page_print
        if page is None:
            return result,message,page_print
        page_print=PagePrint(person_id=me_person.id,page_id=page.id)
        if 'page_print' in kwargs:
            page_print_text=kwargs['page_print']
            
        if 'printed' in kwargs:
            printed=kwargs['printed']
            page_print.printed=kwargs['printed']

        from .enums import PagePrintTypeEnum        
        if 'draft' in kwargs:
            draft=kwargs['draft']
            if draft:
                page_print.type=PagePrintTypeEnum.DRAFT
        
        

        if 'type' in kwargs: 
            page_print.type=kwargs['type']
        
        if 'official' in kwargs:
            official=kwargs['official']
            if official:
                page_print.type=PagePrintTypeEnum.OFFICIAL
        
        
        page_print.save()

        result=SUCCEED
        message='پرینت صفحه با موفقیت اضافه شد.'
         
        return result,message,page_print


class CommentRepo():

    def __init__(self,request,*args, **kwargs):
        self.objects=Comment.objects
        self.request=request
    def list(self,*args, **kwargs):
        objects=Comment.objects
        if 'search_for' in kwargs:
            objects=objects.filter(Q(comment__contains=kwargs['search_for']))
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        return objects.all()

    def add_comment(self,*args, **kwargs):
        result,message,comment=FAILED,"",None
        me_person=PersonRepo(request=self.request).me
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if me_person is None:
            return None
        if 'comment' in kwargs:
            comment_text=kwargs['comment']
        if comment_text is None:
            return result,message,comment
        comment=Comment(person_id=me_person.id,page_id=page.id,comment=comment_text)
        if 'parent_id' in kwargs:
            parent_id=kwargs['parent_id']
            if parent_id is not None and parent_id>0:
                comment.parent_id=parent_id
        comment.save()
        result=SUCCEED
        message='کامنت با موفقیت اضافه شد.'
        return result,message,comment
    
    def delete_page_comment(self,*args, **kwargs):
        me_person=PersonRepo(request=self.request).me
        if 'comment_id' in kwargs:
            comment_id=kwargs['comment_id']
        # comments=Comment.objects.filter(person_id=me_person.id).filter(pk=comment_id)
        comments=Comment.objects.filter(pk=comment_id)
        comments.delete()
        from utility.log import leolog
        result=SUCCEED
        message="کامنت با موفقیت حذف گردید."
        return result,message
     
class TagRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Tag.objects
        self.request=request
    def tag(self,*args, **kwargs):
        if 'title' in kwargs:
            return Tag.objects.filter(title=kwargs['title']).first()
        if 'tag_id' in kwargs:
            return Tag.objects.filter(pk=kwargs['tag_id']).first()
        if 'pk' in kwargs:
            return Tag.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return Tag.objects.filter(pk=kwargs['id']).first()
        
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
            page=PageRepo(request=self.request).page(page_id=page_id)
            if page is not None:
                return page.tag_set.all()
            objects=objects.filter(page_id=page_id)
             

        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(title__contains=search_for)
        return objects.all()
    def add_tag(self,*args, **kwargs):
        result,message,tags=FAILED,'',[]

        title=kwargs['title']
        page_id=kwargs['page_id']


        tag=self.tag(title=title)
        page=PageRepo(request=self.request).page(page_id=page_id)
        if tag is None:
            tag=Tag(title=title)
            tag.save()

        if page is None:
            message='صفحه پیدا نشد.'
            return result,message,tags 

        pages=tag.pages.all()
        if page in pages:
            tag.pages.remove(page)
            if len(tag.pages.all())==0:
                tag.delete()
        else:
            tag.pages.add(page.id)
        tag.save()
        result=SUCCEED
        message='تگ با موفقیت اضافه شد.'
        tags=page.tag_set.all()
        return result,message,tags 

class LikeRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Like.objects
        self.request=request
        self.me_person=PersonRepo(request=request).me
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'person_id' in kwargs:
            objects=objects.filter(person_id=kwargs['person_id'])
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        return objects.all()
    def toggle_like(self,*args, **kwargs):
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if page is None:
            return None
        me_person=PersonRepo(request=self.request).me
        if me_person is None:
            return None
        likes=Like.objects.filter(page_id=page.id).filter(person_id=me_person.id)
        my_like=False
        if len(likes)==0:
            my_like=Like(page=page,person=me_person)
            my_like.save()
            my_like=True
        else:
            likes.delete()
        likes_count=self.likes_count(page=page)
        return (my_like,likes_count)
    

    def my_like(self,page,*args, **kwargs):
        me_person=PersonRepo(request=self.request).me
        if me_person is None:
            return None
        if page is None:
            return None
        likes=Like.objects.filter(person_id=me_person.id).filter(page_id=page.id)
        return len(likes)>0
    
    def likes_count(self,*args, **kwargs):
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if page is None:
            return None
        return len(Like.objects.filter(page_id=page.pk))    
    def my_likes(self,*args, **kwargs):
        if self.me_person is not None:
            return Like.objects.filter(person_id=self.me_person.id)
 
    

class LinkRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Link.objects
        self.request=request
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            objects=objects.filter(Q(title__contains=kwargs['search_for']))
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
            objects=objects.filter(page_id=page_id)
        return objects.all()
    def add_link(self,*args, **kwargs):
        result,message,link=FAILED,'',None
        result=SUCCEED
        link=Link(**kwargs)
        # link.url=url
        # link.title=title
        # link.page_id=page_id
        link.save()
        message='لینک با موفقیت اضافه شد.'
        return result,message,link 

class DownloadRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Download.objects
        self.request=request
    def download(self,*args, **kwargs):
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'download_id' in kwargs:
            return self.objects.filter(pk=kwargs['download_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            objects=objects.filter(Q(title__contains=kwargs['search_for']))
        
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
            objects=objects.filter(page_id=page_id)
        return objects.all()
     
    


    def add_download(self,title,file,priority=1000,*args, **kwargs):
        result,message,download=FAILED,'',None
        can_write=False
        page=PageRepo(request=self.request).page(page_id=kwargs['page_id'])
         
        if self.request.user.has_perm(APP_NAME+".change_page"):
            can_write=True
         
        if page is None or not can_write:
            message='صفحه وجود ندارد.'
            return result,message,download

        if page.app_name=='web':
            is_open=True
        else:
            is_open=False
        me_person=PersonRepo(request=self.request).me
        if me_person is None:
            message='پروفایل وجود ندارد.'
            return result,message,download
        download=Download(icon_fa="fa fa-download",title=title,is_open=is_open,file=file,priority=priority,page_id=page.id,person_id=me_person.id)
        download.save()
        result=SUCCEED
        message='دانلود با موفقیت اضافه شد.'
        download.persons.add(me_person)
        return result,message,download


class LocationRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.person=PersonRepo(*args, **kwargs).me
        self.objects = Location.objects
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'location_id' in kwargs:
            objects=objects.filter(location_id=kwargs['location_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects.all()
    
    
    def add_page_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_location"):
            return None
        location=LocationRepo(request=self.request).location(*args, **kwargs)
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if page is None:
            return
        if location is None:
            return
        page.locations.add(location.id)
        return location



    def location(self, *args, **kwargs):
        if 'location_id' in kwargs:
            return self.objects.filter(pk=kwargs['location_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
            

    def add_location(self,*args, **kwargs):
        from utility.log import leolog
        result,message,location=FAILED,'',self
        if not self.user.has_perm(APP_NAME+".add_location"):
            return result,message,None
        location=Location()
        if 'location' in kwargs:
            location1=kwargs['location']
        if 'title' in kwargs:
            location.title=kwargs['title']
        if 'location' in kwargs:
            location.location=kwargs['location']
        if 'latitude' in kwargs:
            location.latitude=kwargs['latitude']
        if 'longitude' in kwargs:
            location.longitude=kwargs['longitude']
        location.creator=self.person
        (result,message,location)=location.save()
        if 'page_id' in kwargs and kwargs['page_id'] is not None:
            page_id=kwargs['page_id']
            page=PageRepo(request=self.request).page(pk=page_id)
            if page is not None and location is not None:
                page.locations.add(location.id)
        return result,message,location
    
    def search(self,search_for):
        objects = self.objects.filter(title__contains=search_for)
        return objects 

    
        
class AreaRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.person=PersonRepo(*args, **kwargs).me
        self.objects = Area.objects
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        if 'location_id' in kwargs:
            objects=objects.filter(location_id=kwargs['location_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(location__title__contains=kwargs['search_for'])
        return objects.all()
    def add_area(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_area"):
            return None
        area=Area()
        if 'code' in kwargs:
            area.code=kwargs['code']
        if 'title' in kwargs:
            area.title=kwargs['title']
        if 'color' in kwargs:
            area.color=kwargs['color']
        if 'area' in kwargs:
            area.area=kwargs['area']
        area.save()
         
        return area

    def area(self, *args, **kwargs):
        if 'area_id' in kwargs:
            return self.objects.filter(pk=kwargs['area_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()