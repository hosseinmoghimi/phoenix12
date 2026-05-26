
from django.utils.translation import gettext as _
from utility.enums import UnitNameEnum
 
from django.db.models import TextChoices

class PARAMETER_NAME_ENUM(TextChoices):
    FARSI_FONT='نام فونت فارسی',_('نام فونت فارسی')
    WIDE_LAYOUT='پنل گسترده تمام صفحه',_('پنل گسترده تمام صفحه')   
     
class EventStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    IN_PROGRESS="در جریان",_("در جریان")
    READY="آماده تحویل",_("آماده تحویل")
    APPROVED="تایید شده",_("تایید شده")
    DELIVERED="تحویل شده",_("تحویل شده")
    CANCELED="کنسل شده",_("کنسل شده")
    ROLL_BACKED="برگشت از تحویل",_("برگشت از تحویل")
    FINISHED="تایید نهایی شده",_("تایید نهایی شده")
    PASSED="پاس شده",_("پاس شده")
    FROM_PAST="مانده حساب از قبل",_("مانده حساب از قبل")
