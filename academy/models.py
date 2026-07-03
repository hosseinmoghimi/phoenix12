from django.db import models
from core.models import LinkHelper,Page,reverse,STATIC_URL
from django.utils.translation import gettext as _ 
from .apps import APP_NAME

class Course(models.Model,LinkHelper):

    title=models.CharField(_("title"), max_length=50)
    app_name=APP_NAME
    class_name="course"
    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        from utility.constants import SUCCEED,FAILED
        super(Course,self).save()
        return SUCCEED,'واحد درسی با موفقیت ذخیره شد.',self


class Word(Page):
     

    class Meta:
        verbose_name = _("Word")
        verbose_name_plural = _("Words")
 

    def save(self,*args, **kwargs):
        from utility.constants import SUCCEED,FAILED
        
        if self.class_name is None or self.class_name =='':
            self.class_name="word"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME

        super(Word,self).save()
        return SUCCEED,'کلمه با موفقیت ذخیره شد.',self
    

    def delete(self,*args, **kwargs):
        for word in Word.objects.filter(parent_id=self.id):
            word.parent_id=self.parent_id 
            super(Word,word).save() 
        super(Word,self).delete() 
    
    def get_breadcrumb_link(self):
            aaa=f"""
                        <li class="breadcrumb-item"><a href="{self.get_absolute_url()}">
                        <span class="farsi mx-2">
                        <img class="rounded" width="32" src="{self.thumbnail}">
                        {self.title}
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
                    <li class="breadcrumb-item"><a href="{reverse('academy:word',kwargs={'pk':0})}">
                        <span class="farsi mx-2">
                        <img class="rounded" width="32" src="{STATIC_URL}{APP_NAME}/img/logo.png">
                        Home
                        </span>
                        </a></li> 

                        {self.get_breadcrumb_link()}
                    </ol>
                    </nav>
            """

 