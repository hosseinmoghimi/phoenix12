from django.db import models
from core.models import LinkHelper,Page
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