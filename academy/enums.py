

from django.utils.translation import gettext as _
from django.db.models import TextChoices


class AttendanceStatusEnum(TextChoices):
    ABSENT2="غایب غیر موجه",_("غایب غیر موجه")
    ABSENT1="غایب موجه",_("غایب موجه")
    PRESENT="حاضر",_("حاضر")
    DELAYED="تاخیر",_("تاخیر")
 
class ScoreTypeEnum(TextChoices):
    FINAL="نهایی",_("نهایی")
    MID="میان ترم",_("میان ترم")
    INIT="ارزیابی اولیه",_("ارزیابی اولیه")
    MISC="سایر",_("سایر")