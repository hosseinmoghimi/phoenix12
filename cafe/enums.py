

from django.utils.translation import gettext as _
from django.db.models import TextChoices


class OrderStatusEnum(TextChoices):
    CUSTOMER_ENTERANCE="در حال استقرار",_("در حال استقرار") 
    SERVING="در حال پذیرایی",_("در حال پذیرایی")
    FINISHED="اتمام یافته",_("اتمام یافته")
    CHOOSING="در حال انتخاب",_("در حال انتخاب")
    WAITING_TO_SERVE="در انتظار سرویس",_("در انتظار سرویس")
    FREE="آزاد",_("آزاد")

def get_table_status_color(status):
    if status==OrderStatusEnum.FREE:
        return "success"
    
    if status==OrderStatusEnum.CUSTOMER_ENTERANCE:
        return "success"
    
    if status==OrderStatusEnum.WAITING_TO_SERVE:
        return "danger"
    
    if status==OrderStatusEnum.CHOOSING:
        return "danger"
    
    if status==OrderStatusEnum.SERVING:
        return "primary"
    
    if status==OrderStatusEnum. FINISHED:
        return "success"
    
    return "primary"
    