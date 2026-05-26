from django.utils.translation import gettext as _

from django.db.models import TextChoices

from utility.enums import OperatingSystemNameEnum



class ProjectTypeEnum(TextChoices):
    TYPE_A="تایپ A",_("تایپ A")
    TYPE_B="تایپ B",_("تایپ B")



def StatusColor(project):
    if project.status==ProjectStatusEnum.DRAFT:
        return 'muted'
    if project.status==ProjectStatusEnum.FINISHED:
        return 'success'
    if project.status==ProjectStatusEnum.IN_PROGRESS:
        return 'info'
    if project.status==ProjectStatusEnum.STARTED:
        return 'warning'
    if project.status==ProjectStatusEnum.SUSPENDED:
        return 'danger'
    return 'primary'


class ProjectStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    STARTED="شروع شده",_("شروع شده")
    IN_PROGRESS="در جریان",_("در جریان")
    FINISHED="پایان یافته",_("پایان یافته") 
    SUSPENDED="معلق",_("معلق") 


class TicketTypeEnum(TextChoices):
    TYPE_A="تایپ A",_("تایپ A")
    TYPE_B="تایپ B",_("تایپ B")
    TYPE_C="تایپ C",_("تایپ C")



class TicketStatusEnum(TextChoices):
    STARTED="شروع شده",_("شروع شده")
    IN_PROGRESS="در جریان",_("در جریان")
    FINISHED="پایان یافته",_("پایان یافته") 

