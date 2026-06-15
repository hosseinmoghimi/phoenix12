from email.policy import default
from django.db import models
from django.forms import CharField
from django.utils.translation import gettext as _
from core.models import LinkHelper
from .apps import APP_NAME
from django.shortcuts import reverse
from core.models import Page
from phoenix.server_settings import STATIC_URL
# Create your models here.
class Folder(models.Model,LinkHelper):
    
    name=models.CharField(_("name"), max_length=100)
    parent=models.ForeignKey("folder",related_name="childs",null=True,blank=True, verbose_name=_("parent"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_updated=models.DateTimeField(_("date_updated"), auto_now=True, auto_now_add=False)
    persons=models.ManyToManyField("authentication.person",blank=True, verbose_name=_("persons"))
    priority=models.IntegerField(_("ترتیب"),default=1000)
    owner=models.ForeignKey("authentication.person", verbose_name=_("person"),related_name="folders_owned",null=True,blank=True, on_delete=models.CASCADE)
    class_name='folder'
    app_name=APP_NAME
    @property
    def title(self):
        return self.name
    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        super(Folder,self).save()
        if self.owner is not None:
            self.persons.add(self.owner)

    def get_breadcrumb_link(self):
        aaa=f"""
                    <li class="breadcrumb-item"><a href="{self.get_absolute_url()}">
                    <span class="farsi">
                    {self.name}
                    </span>
                    </a></li> 
                    
                    
                    """
        if self.parent is None:
            return aaa
        return self.parent.get_breadcrumb_link()+aaa
    def get_breadcrumb(self):
        return f"""
        
                <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    {self.get_breadcrumb_link()}
                </ol>
                </nav>
        """
    def thumbnail(self):
        return STATIC_URL+'archive/img/pages/thumbnail/folder.png'

# class FolderPermission(models.Model):
#     folder=models.ForeignKey("folder", verbose_name=_("folder"), on_delete=models.CASCADE)
#     profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
#     can_write=models.BooleanField(_("can write"),default=False)
    

#     class Meta:
#         verbose_name = _("FolderPermission")
#         verbose_name_plural = _("FolderPermissions")

#     def __str__(self):
#         return f"""{"rw" if self.can_write else "r"} ^ {self.folder.title} @ {self.person.name} """
 
class File(Page):
    folder=models.ForeignKey("folder",related_name="files", verbose_name=_("folder"), on_delete=models.CASCADE)
    is_public=models.BooleanField(_("is_public?"),default=False)


    @property
    def name(self):
        return self.title
    

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")
 

    def save(self,*args, **kwargs):
        if self.app_name is None or self.app_name=='':
            self.app_name=APP_NAME
        if self.class_name is None or self.class_name=='':
            self.class_name='file'
        return super(File,self).save(*args, **kwargs)