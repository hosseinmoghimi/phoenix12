

from django.utils.translation import gettext as _
from django.db.models import TextChoices


class TempEnum(TextChoices):
    CUSTOMER_ENTERANCE="در حال استقرار",_("در حال استقرار") 
    SERVING="در حال پذیرایی",_("در حال پذیرایی")
    FINISHED="اتمام یافته",_("اتمام یافته")
    CHOOSING="در حال انتخاب",_("در حال انتخاب")
    WAITING_TO_SERVE="در انتظار سرویس",_("در انتظار سرویس")
    FREE="آزاد",_("آزاد")
 