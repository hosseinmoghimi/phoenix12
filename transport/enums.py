from core import enums as CoreEnums
from django.db.models import TextChoices
from django.utils.translation import gettext as _
from utility.enums import WeightUnitEnum

    
class TripStatusEnum(TextChoices):
    REQUESTED="درخواست شده",_("درخواست شده")
    APPROVED="تأیید شده",_("تأیید شده")
    CANCELED="کنسل شده",_("کنسل شده")
    DELIVERED="تحویل شده",_("تحویل شده")


class MaintenanceTypesEnum(TextChoices):
    WASH="شستشو",_("شستشو") 
    FUEL='سوخت',_('سوخت')
    REPAIR_ENGINE='تعمیر موتور',_('تعمیر موتور') 
    INSURANCE='بیمه',_('بیمه')
    ELECTRIC='برق خودرو',_('برق خودرو')
    TIRE='لاستیک',_('لاستیک')
    BODY ='بدنه',_('بدنه')
    SUSPENTION ='جلوبندی',_('جلوبندی')
    NEW_OIL='تعویض روغن',_('تعویض روغن') 


class WorkEventEnum(TextChoices):
    FLAT_TIRE='لاستیک پنچر',_('لاستیک پنچر')
    BROKEN_GLASS="شیشه شکسته",_("شیشه شکسته")
    CRASH1="خسارت مالی",_("خسارت مالی")
    CRASH2="خسارت جانی",_("خسارت جانی")
    

class VehicleBrandEnum(TextChoices):
    TOYOTA='تویوتا',_('تویوتا')
    PEUGEOT='پژو',_('پژو')
    BENZ='بنز',_('بنز')
    ISUZU='ایسوزو',_('ایسوزو')
    SCANIA='اسکانیا',_('اسکانیا')
    MAZDA='مزدا',_('مزدا')
    VOLVO='ولوو',_('ولوو')
    PISHTAZ='پیشتاز',_('پیشتاز')
    CATERPILAR='کاترپیلار',_('کاترپیلار')
    HYUNDAI='هیوندای',_('هیوندای')
    HOWO='هووو',_('هووو')
    DONG_FENG='دانگ فنگ',_('دانگ فنگ')
    SAIPA='سایپا',_('سایپا')
    DAF='داف',_('داف')
    IRAN_KHODRO='ایران خودرو',_('ایران خودرو')
    XCMG='XCMG',_('XCMG')
    

class HazineEnum(TextChoices):
    SOBHANE='صبحانه',_('صبحانه')
    NAHAR='نهار',_('نهار')
    SHAM='شام',_('شام')
    PARKING='پارکینگ',_('پارکینگ')
    AVAREZ='عوارض',_('عوارض')
    ANAM='انعام',_('انعام')
    HAMAM='حمام',_('حمام')
    SIMCARD='شارژ سیمکارت',_('شارژ سیمکارت')
    INTERNET='شارژ اینترنت',_('شارژ اینترنت')
    GENERAL="کل صورت خرجکرد",_("کل صورت خرجکرد")


class VehicleColorEnum(TextChoices):
    SEFID='سفید',_('سفید')
    SIAH='سیاه',_('سیاه')
    NOK_MEDADI='نوک مدادی',_('نوک مدادی')
    DOLPHINI='دلفینی',_('دلفینی')
    BEZH='بژ',_('بژ')
    GHERMEZ='قرمز',_('قرمز')


class VehicleTypeEnum(TextChoices):
    MOTORCYCLE='موتورسیکلت',_('موتورسیکلت')
    TRUCK='وانت',_('وانت')
    SEDAN='سواری',_('سواری')
    BUS='اتوبوس',_('اتوبوس')
    TAXI='تاکسی',_('تاکسی')
    GRADER='گریدر',_('گریدر')
    LOADER='لودر',_('لودر')
    TRAILER='تریلی',_('تریلی')
    CONTAINER='کانتینر',_('کانتینر')
    SEPERATOR='سپراتور',_('سپراتور')
    TRUCK2='خاور',_('خاور')