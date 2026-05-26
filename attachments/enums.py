

from django.utils.translation import gettext as _
from utility.enums import UnitNameEnum
 
from django.db.models import TextChoices

class PagePrintTypeEnum(TextChoices):
    DRAFT='پیش نویس',_('پیش نویس')
    OFFICIAL='رسمی',_('رسمی')