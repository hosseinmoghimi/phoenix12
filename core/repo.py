from .models import Page,FAILED,SUCCEED,Event
from django.db.models import Q
from .apps import APP_NAME 
from authentication.repo import PersonRepo
 
class Repo():
    def __init__(self,request,*args, **kwargs):  
        
        self.app_name=APP_NAME
        self.request=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        self.person=None
        self.request=request
        self.person=PersonRepo(request=self.request).me
    def log(self,*args, **kwargs): 

            # if 'title' in kwargs:            
            #     log.title=kwargs['title']
            # if 'url' in kwargs:     
            #     log.url=kwargs['url']
            # if 'app_name' in kwargs:     
            #     log.app_name=kwargs['app_name']
            # if 'person' in kwargs:            
            #     log.person=kwargs['person'] 
            # if 'person_id' in kwargs:            
            #     log.person_id=kwargs['person_id']
            # if 'description' in kwargs:            
            #     log.description=kwargs['description']
        from log.repo import LogRepo
        LogRepo(request=self.request).add_log(app_name=self.app_name,person=self.person,**kwargs)

class PageRepo(Repo):
    def __init__(self,request,*args, **kwargs):
        super(PageRepo,self).__init__(request=request,*args, **kwargs)
        self.objects=Page.objects

    def page(self,*args, **kwargs):
        page=None
        if 'page' in kwargs:
            page=kwargs['page']
            return page
        if 'page_id' in kwargs:
            page=self.objects.filter(pk=kwargs['page_id']).first()
        if 'pk' in kwargs:
            page=self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            page=self.objects.filter(pk=kwargs['id']).first()
        return page 

    def list(self,*args, **kwargs):
        objects=self.objects
        if 'meta_data' in kwargs:
            meta_data=kwargs['meta_data']
            objects=objects.filter(meta_data=meta_data)
        if 'ids' in kwargs:
            ids=kwargs['ids']
            objects=objects.filter(id__in=ids)

        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            id=0
            try:
                id=int(search_for) 
            except:
                pass
            objects=objects.filter(Q(title__contains=search_for) |Q(meta_data=search_for) |Q(id=id))
        return objects.all().order_by('priority')
    def set_thumbnail_header(self,*args, **kwargs):
        if not self.request.user.has_perm("core.change_page"):
            return
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if page is None:
            return

        if 'title' in kwargs and kwargs['title']:
            title=kwargs['title']
            if title is not None and title:
                page.title=title
                page.save()

        if 'color' in kwargs and kwargs['color']:
            page.color=kwargs['color']
            page.save()


        if 'clear_thumbnail' in kwargs and kwargs['clear_thumbnail']:
            page.thumbnail_origin=None
        else:
            if 'thumbnail' in kwargs:
                thumbnail=kwargs['thumbnail']
                if thumbnail is not None:
                    page.thumbnail_origin=thumbnail
                    page.save()



        if 'clear_header' in kwargs and kwargs['clear_header']:
            page.header_origin=None
        else:
            if 'header' in kwargs:
                header=kwargs['header']
                if header is not None:
                    page.header_origin=header
                    page.save()
        return page

    
    def set_priority(self,*args, **kwargs):
        result,message,priority=FAILED,"",None
        if not self.request.user.has_perm(APP_NAME+".change_page"):
            return result,message,priority
        priority=kwargs['priority']
        page_id=kwargs['page_id']
        
         

        page=Page.objects.filter(pk=page_id).first()
        if page is not None:
            page.priority=priority
            page.save()

        result=SUCCEED

        return result,message,priority

    
    def add_related_page(self,*args, **kwargs):
        can_write=False
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if self.request.user.has_perm(APP_NAME+".change_page"):
            can_write=True 
        if page is None or not can_write:
            return

        
        page_id=0
        related_page_id=0
        bidirectional=True
        add_or_remove=True
        if 'page_id' in kwargs:
            page_id=kwargs['page_id']
        if 'related_page_id' in kwargs:
            related_page_id=kwargs['related_page_id']
        if 'bidirectional' in kwargs:
            bidirectional=kwargs['bidirectional']
        if 'add_or_remove' in kwargs:
            add_or_remove=kwargs['add_or_remove']
        if add_or_remove is None:
            add_or_remove=True
        page=self.page(page_id=page_id)
        related_page=self.page(page_id=related_page_id)
        if page is None or related_page is None:
            return None
        if add_or_remove:
            page.related_pages.add(related_page)
            if bidirectional:
                related_page.related_pages.add(page)
            return related_page
        else:
            page.related_pages.remove(related_page)
            if bidirectional:
                related_page.related_pages.remove(page)
            return related_page

   
class EventRepo():
    def __init__(self,request,*args, **kwargs):
        self.objects=Event.objects
        self.request=request
    def event(self,*args, **kwargs):
        event=None
        if 'event' in kwargs:
            event=kwargs['event']
            return event
        if 'event_id' in kwargs:
            event=self.objects.filter(pk=kwargs['event_id']).first()
        if 'pk' in kwargs:
            event=self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            event=self.objects.filter(pk=kwargs['id']).first()
        return event 

    def list(self,*args, **kwargs):
        objects=self.objects
        if 'meta_data' in kwargs:
            meta_data=kwargs['meta_data']
            objects=objects.filter(meta_data=meta_data)
        if 'ids' in kwargs:
            ids=kwargs['ids']
            objects=objects.filter(id__in=ids)

        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            id=0
            try:
                id=int(search_for) 
            except:
                pass
            objects=objects.filter(Q(title__contains=search_for) |Q(meta_data=search_for) |Q(id=id))
        return objects.all()
     
    def add_event(self,*args, **kwargs):
        result,message,event=FAILED,'',None
        event=Event(app_name='core',class_name='event')
        if 'title' in kwargs:
            event.title=kwargs['title']
        if 'description' in kwargs:
            event.description=kwargs['description']
        if 'event_datetime' in kwargs:
            event.event_datetime=kwargs['event_datetime']
        if 'start_datetime' in kwargs:
            event.start_datetime=kwargs['start_datetime']
        if 'end_datetime' in kwargs:
            event.end_datetime=kwargs['end_datetime']
        event.save()
        result=SUCCEED
        message='رویداد با موفقیت اضافه شد'
        return result,message,event