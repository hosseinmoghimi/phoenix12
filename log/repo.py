from .models import Log
from .apps import APP_NAME

class LogRepo():
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Log.objects.order_by('-date_added') 
        from authentication.repo import PersonRepo
        self.person=PersonRepo(request=self.request).me
        if self.user.has_perm(APP_NAME+".view_log"):
            self.objects = Log.objects
        elif self.person is not None:
            self.objects=Log.objects.filter(person_id=self.person.id)
        else:
            self.objects = Log.objects.filter(pk=0)


    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        if 'url' in kwargs:
            url=kwargs['url']
            objects = objects.filter(url=url) 
        return objects

    def log(self, *args, **kwargs):
        if 'log_id' in kwargs:
            return self.objects.filter(pk= kwargs['log_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()    
        
    def add_log(self,*args, **kwargs):
        log=Log()
        if 'title' in kwargs:            
            log.title=kwargs['title']
        if 'url' in kwargs:     
            log.url=kwargs['url']
        if 'app_name' in kwargs:     
            log.app_name=kwargs['app_name']
        if 'person' in kwargs:            
            log.person=kwargs['person'] 
        if 'person_id' in kwargs:            
            log.person_id=kwargs['person_id']
        if 'description' in kwargs:            
            log.description=kwargs['description']
        from utility.log import leolog
        # leolog(log=log)
        log.save()
        return log