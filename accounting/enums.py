from django.utils.translation import gettext as _
from utility.enums import UnitNameEnum
from .enums import *
from django.db.models import TextChoices


class InvoiceLineStatusEnum(TextChoices):
    BOXED='نو',_('نو') 
    UN_BOXED='کارکرده',_('کارکرده') 
    UN_BOXED_CLEAN='کارکرده در حد نو',_('کارکرده در حد نو') 
    UN_BOXED_UN_USED='نو بدون جعبه',_('نو بدون جعبه') 
    REPAIRED='تعمیر شده',_('تعمیر شده')
    BROKEN='خراب',_('خراب')
    DAMAGED='داغون',_('داغون')
    FAKE='قلابی',_('قلابی')
    ORIGINAL='اصلی',_('اصلی')

class PersonCategoryEnum(TextChoices):
    DEFAULT='پیش فرض',_('پیش فرض')
    CUSTOMER='مشتری',_('مشتری')
    SUPPLIER='فروشنده',_('فروشنده')
    PERSONNEL='پرسنل',_('پرسنل')
    SAHAMDAR='سهامدار',_('سهامدار')
    CONTRACTOR='پیمانکار',_('پیمانکار')
    EMPLOYER='کارفرما',_('کارفرما')
    COST='هزینه',_('هزینه')

class RequestStatusEnum(TextChoices):
    INITIAL='درخواست اولیه',_('درخواست اولیه')
    DENIED="رد شده",_("رد شده")
    ACCEPTED="پذیرفته شده",_("پذیرفته شده")
    DELIVERED="تحویل شده",_("تحویل شده")


class FinancialDocumentStatusEnum(TextChoices):
    DRAFT='پیش نویس',_('پیش نویس')
    DENIED='رد شده',_('رد شده')
    ACCEPTED='تایید شده',_('تایید شده')


class FinancialYearStatusEnum(TextChoices):
    SUSPEND='معلق',_('معلق')
    LOCKED='بسته شده',_('بسته شده')
    IN_PROGRESS='در جریان',_('در جریان')
    DRAFT='پیش نویس',_('پیش نویس')
    TEMP='موقتی',_('موقتی')

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


class AccountNatureEnum(TextChoices):
    BESTANKAR="بستانکار",_("بستانکار")
    ONLY_BESTANKAR="فقط بستانکار",_("فقط بستانکار")
    BEDEHKAR="بدهکار",_("بدهکار")
    ONLY_BEDEHKAR="فقط بدهکار",_("فقط بدهکار")
    FREE="بدون کنترل",_("بدون کنترل")

    

class PaymentMethodEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    # NO_PAYMENT="پرداخت نشده",_("پرداخت نشده")
    MOBILE_BANK="همراه بانک",_("همراه بانک")
    PRODUCT="فروش کالا",_("فروش کالا")
    SERVICE="فروش خدمات",_("فروش خدمات")
    IN_CASH="نقدی",_("نقدی")
    CHEQUE="چک",_("چک")
    POS="کارتخوان",_("کارتخوان")
    BANK_FISH="فیش بانکی",_("فیش بانکی")
    CARD="کارت به کارت",_("کارت به کارت")


class FinancialEventStatusEnum(TextChoices):
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


 

 