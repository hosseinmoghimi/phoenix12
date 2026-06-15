from archive.models import Folder,File
from django.db.models import Q
from authentication.repo import PersonRepo
from .apps import APP_NAME
    

class FolderRepo:
    def __init__(self,request, *args, **kwargs): 
        self.request = request 
        self.person = PersonRepo(request=request).me
        self.objects = Folder.objects.order_by('name')
        if self.request.user.has_perm(APP_NAME+".view_folder"):
            self.objects = self.objects.all()
        elif self.person is not None:
            self.objects = self.person.folder_set.all()
        else:
            self.objects = self.objects.filter(pk=0)

    def create_folder(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_folder"):
            return
        folder=Folder(*args, **kwargs)
        if self.person is not None:
            folder.owner=self.person
        folder.save(*args, **kwargs)
        return folder
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'parent_id' in kwargs:
            objects = objects.filter(parent_id=kwargs['parent_id'])
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            objects = objects.filter(Q(name__contains=kwargs['search_for']))
        return objects
    def get_root(self,*args, **kwargs):
        folder=Folder.objects.filter(pk=1).first()
        if folder is None:
            if not 'name' in kwargs:
                kwargs['name']="خانه"
            folder=Folder(*args, **kwargs)
            folder.save()
        return folder
    def folder(self,*args, **kwargs):
        if 'folder' in kwargs and kwargs['folder'] is not None:
            folder=kwargs['folder']
            return folder
        if 'name' in kwargs and kwargs['name'] is not None:
            return self.objects.filter(name= kwargs['name']).first()
        
        
        if 'pk' in kwargs and kwargs['pk'] is not None:
            pk=kwargs['pk']
        if 'id' in kwargs and kwargs['id'] is not None:
            pk=kwargs['id']
        if 'folder_id' in kwargs and kwargs['folder_id'] is not None:
            pk=kwargs['folder_id']
        
        if pk==1:
            folder=self.get_root(*args, **kwargs)
            return folder
        else:
            folder=self.objects.filter(pk=pk).first()
        if self.person is None or folder is None:
            return
        if self.request.user.has_perm(APP_NAME+".view_fodler"):
            return folder
        if self.person in folder.profiles.all() or self.person.pk==folder.owner.pk:
            return folder 
   

class FileRepo:
    def __init__(self,request, *args, **kwargs):
        self.request = request
        self.person = PersonRepo(request=request).me
        self.objects = File.objects.all()
        if self.request.user.has_perm(APP_NAME+".view_file"):
            self.objects = self.objects.all()
        elif self.person is not None:
            self.objects = self.objects.filter(Q(is_public=True)|Q(folder__owner_id=self.person.pk))
        else:
            self.objects = self.objects.filter(pk=0)

    def create_file(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_file"):
            return
        file=File()
        if 'title' in kwargs:
            file.title=kwargs['title']
        if 'folder_id' in kwargs:
            file.folder_id=kwargs['folder_id']
        file.save(*args, **kwargs)
        return file
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'folder_id' in kwargs:
            objects = objects.filter(folder_id=kwargs['folder_id'])
        if 'search_for' in kwargs:
            objects = objects.filter(Q(title__contains=kwargs['search_for'])|Q(description__contains=kwargs['search_for']))
        return objects
    def file(self,*args, **kwargs):
        if 'file' in kwargs and kwargs['file'] is not None:
            file=kwargs['folder']
            return file
        
        
        pk=0 
        if 'pk' in kwargs and kwargs['pk'] is not None:
            pk=kwargs['pk']
        if 'id' in kwargs and kwargs['id'] is not None:
            pk=kwargs['id']
        if 'file_id' in kwargs and kwargs['file_id'] is not None:
            pk=kwargs['file_id']
        
        file=self.objects.filter(pk=pk).first()
        return file 
   