from django.db import models
from django.shortcuts import reverse
from phoenix.server_settings import ADMIN_URL
from utility.enums import AppNameEnum
from utility.models import LinkHelper,DateTimeHelper
from .apps import APP_NAME
from django.utils.translation import gettext as _
# from django.conf import settings
# Create your models here.

class Log(models.Model,DateTimeHelper):
    title=models.CharField(_("title"), max_length=500)
    # user=models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True ,verbose_name=_("user"), on_delete=models.SET_NULL)
    person=models.ForeignKey("authentication.person",null=True,blank=True ,related_name="logs",verbose_name=_("person"), on_delete=models.SET_NULL)
    url=models.CharField(_("url"),null=True,blank=True, max_length=50000)
    description=models.CharField(_("description"),null=True,blank=True, max_length=50000)
    app_name=models.CharField(_("app_name"),choices=AppNameEnum.choices,null=True,blank=True, max_length=50)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    class_name="log"


    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"
    def get_absolute_url(self):
        return reverse(f"{APP_NAME}:{self.class_name}",kwargs={'pk':self.pk})
    def get_delete_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/delete/"
    

    # @property
    # def profile(self):
    #     from authentication.models import Profile
    #     if self.user is None:
    #         return None
    #     return Profile.objects.filter(user=self.user).first()
    class Meta:
        verbose_name = _("Log")
        verbose_name_plural = _("Logs")

    def __str__(self):
        return self.title +(self.app_name if self.app_name else "")
 