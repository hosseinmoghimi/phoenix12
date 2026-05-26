from django.utils.translation import gettext as _

from django.db.models import TextChoices
from accounting.enums import UnitNameEnum

class ShopLevelEnum(TextChoices):
    GUEST='میهمان',_('میهمان')
    END_USER="خریدار نهایی",_("خریدار نهایی")
    PARTIAL_SELLER="فروشنده جزء",_("فروشنده جزء")
    MASS_SELLER="فروشنده کل",_("فروشنده کل")
    
 