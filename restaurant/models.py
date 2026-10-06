from django.db import models
from core.models import _,reverse,Page,LinkHelper,DateTimeHelper,FAILED,SUCCEED
from .apps import APP_NAME 
from accounting.models import Product


class Food(Product,LinkHelper):
    class_name="food"
    app_name=APP_NAME
    code=models.CharField(_("کد"), max_length=50)
    
    
    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")

    def __str__(self):
        return self.title
 
    def save(self):
        (result,message,table)=FAILED,'',self
         
        super(Food,self).save()   
        result=SUCCEED
        message="غذا با موفقیت اضافه شد."
        return (result,message,table) 
