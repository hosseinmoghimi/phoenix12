from .models import Parameter,Picture
from utility.constants import *
from django.db.models import Q
from core.repo import Repo 
from .apps import APP_NAME

from .log import leolog


class PictureRepo(Repo):
    
    def __init__(self,request,*args, **kwargs):
        super(PictureRepo,self).__init__(request,*args, **kwargs)
        self.app_name=""
        self.request=request
        self.user=None
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user 
        self.objects=Picture.objects.filter(app_name=self.app_name)
    def list(self,*args, **kwargs):
        return self.objects.filter(app_name=self.app_name)
    def picture(self,*args, **kwargs):
        if 'app_name' in kwargs:
            app_name=kwargs['app_name']
            self.app_name=app_name
            self.objects=Picture.objects.filter(app_name=app_name)

        pk=0
        name=""
        picture=None
        if 'name' in kwargs:
            name=kwargs['name']
            if name=="":
                return
            picture= self.objects.filter(app_name=self.app_name).filter(name=name).first()
            if picture is None:
                picture=Picture(app_name=self.app_name,name=name)
                picture.app_name=self.app_name
                picture.name=name
                if 'default' in kwargs:
                    picture.image_origin=kwargs['default']
                picture.save()
                return picture
            # (picture,res) = self.objects.get_or_create(name=name,app_name=self.app_name)
            # picture = self.objects.filter(name=name).filter(app_name=self.app_name).first()
            return picture
        if 'pk' in kwargs:
            pk=kwargs['pk']
        if 'picture_id' in kwargs:
            pk=kwargs['picture_id']
        if pk>0:
            picture= self.objects.filter(pk=pk).first()
        return picture

    def get(self,*args, **kwargs):
        return self.picture(*args, **kwargs)

class ParameterRepo(Repo):    
    def __init__(self,request,*args, **kwargs):
        super(ParameterRepo,self).__init__(request,*args, **kwargs)

        self.request=request
        if request is not None:
            self.user=self.request.user 
        self.objects=Parameter.objects
        if 'app_name' in kwargs :
            self.app_name=kwargs['app_name']
            self.objects=Parameter.objects.filter(app_name=self.app_name)
        else:
            self.app_name=None
        # self.person=PersonRepo(request=self.request).me
        
        if 'force' in kwargs and kwargs['force']:
            self.objects=Parameter.objects.all()
    
    def change_parameter_temp_deleted(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+'.change_parameter'):
            return None
        parameter_id=kwargs['parameter_id'] if 'parameter_id' in kwargs else None
        parameter_name=kwargs['parameter_name'] if 'parameter_name' in kwargs else None
        parameter_value=kwargs['parameter_value'] if 'parameter_value' in kwargs else None
        app_name=self.app_name
        if parameter_id is not None:
            parameter=Parameter.objects.filter(pk=parameter_id).first()
            if parameter is None:
                return None
        elif parameter_name is not None and app_name is not None:
            parameter=Parameter.objects.filter(app_name=app_name).filter(name=parameter_name).first()
            if parameter is None:
                parameter=Parameter(app_name=app_name,name=parameter_name,value_origin="")
                parameter.save()
        
        parameter.origin_value=parameter_value
        parameter.save()
        return parameter

    
    def set(self,*args, **kwargs):
         
        return self.set_parameter(*args, **kwargs)
    
    def set_parameter(self,*args, **kwargs):
         
        value=kwargs['value']
        name=kwargs['name']
        app_name=kwargs['app_name']
        if not self.request.user.has_perm(APP_NAME+'.change_parameter'):
            message='مجوز دسترسی شما برای این کار کافی نمی باشد. '
            return FAILED,message,None
        Parameter.objects.filter(app_name=app_name).filter(name=name).delete()
        if value is None:
            value=name
        parameter=self.parameter()
        parameter.name=name
        parameter.app_name=app_name
        parameter.origin_value=value
        parameter.save()
        message="پارامتر با موفقیت تغییر یافت."
        return SUCCEED,message,parameter
     
    
    
    def parameter(self,*args, **kwargs):
        
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
            self.objects=Parameter.objects.filter(app_name=self.app_name)

        parameter=None
        parameter_name=""
        if 'parameter_name' in kwargs:
            parameter_name=kwargs['parameter_name']
        if 'name' in kwargs:
            parameter_name=kwargs['name']
        parameter= self.objects.filter(name=parameter_name).first()
        if parameter is None:
            default=parameter_name
            if 'default' in kwargs:
                default=kwargs['default']
            
            parameter=Parameter(name=parameter_name,app_name=self.app_name,origin_value=default)
            parameter.save()

        if 'id' in kwargs:
            parameter= self.objects.filter(name=kwargs['id']).first()
        if 'parameter_id' in kwargs:
            parameter= self.objects.filter(name=kwargs['parameter_id']).first()
        if 'pk' in kwargs:
            parameter= self.objects.filter(name=kwargs['pk']).first()
            
        return parameter

        

    def list(self,*args, **kwargs):
        objects= self.objects
        
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
            objects=objects.filter(app_name=self.app_name)
        return objects.all()

