from django.db import models
from core.models import Page,_,LinkHelper,SUCCEED,FAILED
from accounting.models import Product
from .apps import APP_NAME



class Drug(Product):
    class Meta:
        verbose_name = _("Drug")
        verbose_name_plural = _("Drugs")

    def save(self):
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        if self.class_name is None or self.class_name=="":
            self.class_name='drug'
        super(Drug,self).save()
        return SUCCEED,'دارو ذخیره شد.',self