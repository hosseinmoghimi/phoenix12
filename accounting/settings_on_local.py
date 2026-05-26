# from .enums import AccountTypeEnum
from django.db.models import TextChoices
from django.utils.translation import gettext as _
from utility.log import leolog


NO_DUPLICATED_ACCOUNT_NAME=True
NO_DUPLICATED_ACCOUNT_CODE=True 

class AccountTypeEnum(TextChoices):
    GROUP='گروه',_('گروه')
    BASIC='کل',_('کل')
    MOEIN_1='معین 1',_('معین 1')
    MOEIN_2='معین 2',_('معین 2')
    TAFSILI_1='تفصیلی 1',_('تفصیلی 1')
    TAFSILI_2='تفصیلی 2',_('تفصیلی 2')
    TAFSILI_3='تفصیلی 3',_('تفصیلی 3')
    TAFSILI_4='تفصیلی 4',_('تفصیلی 4')
    TAFSILI_5='تفصیلی 5',_('تفصیلی 5')
    TAFSILI_6='تفصیلی 6',_('تفصیلی 6')


ACCOUNT_LEVEL_NAMES= [
    AccountTypeEnum.GROUP,
    AccountTypeEnum.BASIC,
    AccountTypeEnum.MOEIN_1,
    AccountTypeEnum.MOEIN_2,
    AccountTypeEnum.TAFSILI_1,
    AccountTypeEnum.TAFSILI_2,
    AccountTypeEnum.TAFSILI_3,
    AccountTypeEnum.TAFSILI_4,
    AccountTypeEnum.TAFSILI_5,
    AccountTypeEnum.TAFSILI_6,
]
 