from django.utils.translation import gettext as _
from django.db.models import TextChoices


class EmployeeJobEnum(TextChoices):
    MANAGER="مدیر",_("مدیر")
    COFFEE_MAN="باریستا",_("باریستا")
    GUARD="نگهبان",_("نگهبان")
    WORKMAN="کارگر",_("کارگر")
    ACCOUNTANT="حسابدار",_("حسابدار") 