from core import enums as CoreEnums
from django.db.models import TextChoices
from django.utils.translation import gettext as _
from utility.enums import WeightUnitEnum
    
class OilTypeEnum(TextChoices):
    W15_40="روغن موتور 15_40",_("روغن موتور 15_40")
    W20_40="روغن موتور 20_40",_("روغن موتور 20_40")
    W25_40="روغن موتور 25_40",_("روغن موتور 25_40")
    W20_50="روغن موتور 20_50",_("روغن موتور 20_50")
    HYDROLIC="روغن هیدرولیک",_("روغن هیدرولیک")
    BRAKE="روغن ترمز",_("روغن ترمز")

class FilterActionEnum(TextChoices):
    REPLACE="تعویض",_("تعویض")
    BADGIRI='بادگیری',_("بادگیری")

class OilActionEnum(TextChoices):
    TAVIZ_ROGHAN_MOTOR="تعویض روغن موتور",_("تعویض روغن موتور")
    SARRIZ_ROGHAN_MOTOR="سرریز روغن موتور",_("سرریز روغن موتور")
    TAVIZ_ROGHAN_MISC="تعویض روغن متفرقه",_("تعویض روغن متفرقه")
    SARRIZ_ROGHAN_MISC="سرریز روغن متفرقه",_("سرریز روغن متفرقه")
    
class TavaghofCausesEnum(TextChoices):
    JEB="عدم جبهه کاری",_("عدم جبهه کاری")
    TAV='توقف کارگاه',_("توقف کارگاه")
    RAN="نبود راننده",_("نبود راننده")
    SUKHT='نبود سوخت',_("نبود سوخت")
    MAINTENANCE='تعمیرات دستگاه',_("تعمیرات دستگاه")
    SERVICE='سرویس دستگاه',_("سرویس دستگاه")
    DAMAGED='خرابی دستگاه',_("خرابی دستگاه")
    MISC='سایر',_("سایر")
    
    
class FilterTypeEnum(TextChoices):
    OIL="فیلتر روغن",_("فیلتر روغن")
    AIR="فیلتر هوا",_("فیلتر هوا")
    GASOIL="فیلتر گازوئیل",_("فیلتر گازوئیل")
    HYDROLIC="فیلتر هیدرولیک",_("فیلتر هیدرولیک")
    NANO="فیلتر نانو",_("فیلتر نانو")
    AB_GIR="فیلتر آبگیر",_("فیلتر آبگیر")
    TANK="فیلتر تانک",_("فیلتر تانک")
    BOKHAR_KESH="فیلتر بخارکش",_("فیلتر بخارکش")
    MAGNETIC="فیلتر مغناطیسی",_("فیلتر مغناطیسی")
    DAKHELI="فیلتر داخلی",_("فیلتر داخلی")
    BIRUNI="فیلتر بیرونی",_("فیلتر بیرونی")
    CABIN="فیلتر کابین",_("فیلتر کابین")
    SELECTOR="فیلتر سلکتور",_("فیلتر سلکتور")


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
    LOADER='لودر',_('لودر')
    BIL='بیل مکانیکی',_('بیل مکانیکی')
    COMPRESSI='کمپرسی',_('کمپرسی')
    GRADER='گریدر',_('گریدر')
    BOLDOZER='بلدوزر',_('بلدوزر')

    TRAILER='تریلی',_('تریلی')
    TRUCK2='خاور',_('خاور')
    TRUCK='وانت',_('وانت')
    SEDAN='سواری',_('سواری')
    MOTORCYCLE='موتورسیکلت',_('موتورسیکلت')
    BUS='اتوبوس',_('اتوبوس')
    TAXI='تاکسی',_('تاکسی')
    CONTAINER='کانتینر',_('کانتینر')
    SEPERATOR='سپراتور',_('سپراتور')

    

class TavaghofCauseEnum(TextChoices):
    DEFAULT='نامعلوم',_('نامعلوم')
    DAMAGED='خرابی',_('خرابی')
    SERVICE='سرویس',_('سرویس')
