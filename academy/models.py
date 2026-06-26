from django.db import models
from core.models import LinkHelper,Page
from django.utils.translation import gettext as _ 


class Course(models.Model,LinkHelper):

    title=models.CharField(_("title"), max_length=50)

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title
 