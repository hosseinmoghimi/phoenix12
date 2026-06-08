from django.utils.translation import gettext as _

from django.db.models import TextChoices
from accounting.enums import UnitNameEnum
 
class SupplierGradeEnum(TextChoices):
    NEW='جدید',_('جدید')
    EXPEIENCED="با سابقه",_("با سابقه")
    CONFIRMED="تایید شده",_("تایید شده")    
 