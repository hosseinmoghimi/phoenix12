from django.utils.translation import gettext as _
from django.db.models import TextChoices
 
def StatusColor(page=None,color="success"): 
    if page is None:
        return color
    try:
        if page.status=='ss':
            return 'success'
    except:
        pass
  
    return 'primary'
 
class WeightUnitEnum(TextChoices):
    KILO_GRAM="کیلوگرم",_("کیلوگرم")
    GRAM="گرم",_("گرم")
    TON="تن",_("تن")

 
class SignatureStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    REQUESTED="درخواست می شود",_("درخواست می شود"),
    CONFIRMED="تایید می شود",_("تایید می شود"),
    DENIED="رد می شود",_("رد می شود")
    REVIEWED="بررسی می شود",_("بررسی می شود")
    # DELIVERED="تحویل شد",_("تحویل شد")

class UnitNameEnum(TextChoices):
    ADAD="عدد",_("عدد")
    INSTANCE="مورد",_("مورد")
    KILOGERAM="کیلوگرم",_("کیلوگرم")
    GERAM="گرم",_("گرم")
    METER="متر",_("متر")
    METER2="متر مربع",_("متر مربع")
    METER3="متر مکعب",_("متر مکعب")
    LITER="لیتر",_("لیتر")
    MILI_LITER="میلی لیتر",_("میلی لیتر")
    CC="سی سی ",_("سی سی ")
    SHELL="شل",_("شل")
    SERVICE="سرویس",_("سرویس")
    SHAKHEH="شاخه",_("شاخه")
    Node="نود شبکه",_("نود شبکه")
    SHISHEH="شیشه",_("شیشه")
    DASTGAH="دستگاه",_("دستگاه")
    SHEET="ورق",_("ورق")
    TON="تن",_("تن")
    LINE="خط",_("خط")
    PORS="پورس",_("پورس")
    PART="قطعه",_("قطعه")
    Roll="رول",_("رول") 
    TAKHTE="تخته",_("تخته")
    LINK="لینک",_("لینک")
    KHESHAB="خشاب",_("خشاب")
    PERSON="نفر",_("نفر")
    PACK="بسته",_("بسته")
    POCKET="کیسه",_("کیسه")
    SHOT="شات",_("شات")
    SET="ست",_("ست")
    CUP="فنجان",_("فنجان")
    JOFT="جفت",_("جفت")
    DAST="دست",_("دست")
    BOSHKEH="بشکه",_("بشکه")
    GALON="گالن",_("گالن")
    CARTON="کارتن",_("کارتن")
    HOUR="ساعت",_("ساعت")
    MINUTE="دقیقه",_("دقیقه")
    JABE="جعبه",_("جعبه")
    SABAD="سبد",_("سبد")
    RAS="راس",_("راس")
    BOTTLE="بطری",_("بطری")
    JELD="جلد",_("جلد")
    SHIFT="شیفت",_("شیفت")
    DAY="روز",_("روز")
    MONTH="ماه",_("ماه")
    YEAR="سال",_("سال")
    SESSION="جلسه",_("جلسه")


class OperatingSystemNameEnum(TextChoices):
    WINDOWS_12='Windows 12',_('Windows 12')
    WINDOWS_11='Windows 11',_('Windows 11')
    WINDOWS_10='Windows 10',_('Windows 10')
    WINDOWS_8_1='Windows 8.1',_('Windows 8.1')
    WINDOWS_8='Windows 8',_('Windows 8')
    WINDOWS_7='Windows 7',_('Windows 7')
    WINDOWS_XP='Windows XP',_('Windows XP')
    WIN_SERVER_2012='Windows Server 2012',_('Windows Server 2012')
    WIN_SERVER_2018='Windows Server 2018',_('Windows Server 2018')
    WIN_SERVER_2020='Windows Server 2020',_('Windows Server 2020')
    WIN_SERVER_2022='Windows Server 2022',_('Windows Server 2022')
    WIN_SERVER_2024='Windows Server 2024',_('Windows Server 2024')
    LINUX='Linux',_('Linux')
    LINUX_UBUNTU='Linux Ubuntu',_('Linux Ubuntu')
    LINUX_UBUNTU_24='Linux Ubuntu 2024',_('Linux Ubuntu 2024')
    ANDROID='ANDROID',_('ANDROID')
    IOS='IOS',_('IOS')
  
class TextDirectionEnum(TextChoices):
    Rtl='rtl',_('rtl')
    Ltr='ltr',_('ltr')

def BS_ColorCode(bs_color):
    if bs_color=='success':
        return "#28a745"
    if bs_color=='danger':
        return "#dc3545"
    if bs_color=='warning':
        return "#ffc107"
    if bs_color=='muted':
        return "#34345455"
    if bs_color=='info':
        return "#17a2b8"
    if bs_color=='rose':
        return "#34345455"
    if bs_color=='secondary':
        return "#6c757d"
    if bs_color=='light':
        return "#f8f9fa"
    if bs_color=='dark':
        return "#343a40"
    if bs_color=='primary':
        return "#007bff"
    if bs_color=='blue':
        return "#007bff"
    if bs_color=='indigo':
        return "#6610f2"
    if bs_color=='purple':
        return "#6f42c1"
    if bs_color=='pink':
        return "#e83e8c"
    if bs_color=='red':
        return "#dc3545"
    if bs_color=='orange':
        return "#fd7e14"
    if bs_color=='yellow':
        return "#ffc107"
    if bs_color=='green':
        return "#28a745"
    if bs_color=='teal':
        return "#20c997"
    if bs_color=='cyan':
        return "#17a2b8"
    if bs_color=='white':
        return "#fff"
    if bs_color=='gray':
        return "#6c757d"
    if bs_color=='gray-dark':
        return "#343a40"


  
class GenderEnum(TextChoices):
    MALE="مرد" , _("مرد")
    FEMALE="زن" , _("زن")
    BOTH="هردو" , _("هردو")
    NONE="هیچکدام" , _("هیچکدام")
    INDEPENDENT="مستقل" , _("مستقل")
    OTHERS="دیگر" , _("دیگر")

    
class PersonPrefixEnum(TextChoices):
    MR="آقای",_("آقای")
    MRS="خانم",_("خانم")
    COMPANY="شرکت",_("شرکت")
    DR="دکتر",_("دکتر")
    ENGINEER="مهندس",_("مهندس")
    COMPLEX=" مجتمع",_(" مجتمع")
    SHOP="فروشگاه",_("فروشگاه")
    UNIVERSITY="دانشگاه",_("دانشگاه")
    RESTAURANT="رستوران",_("رستوران")
    SCHOOL="آموزشگاه",_("آموزشگاه")
    OFFICE="اداره",_("اداره")
  
class AppNameEnum(TextChoices):
    projectmanager='projectmanager',_('projectmanager')
    accounting='accounting',_('accounting')
    web='web',_('web')
    transport='transport',_('transport')
    log='log',_('log')
    map='map',_('map')
    market='market',_('market')
    stock='stock',_('stock')
    authentication='authentication',_('authentication')
    dashboard='dashboard',_('dashboard')
    polls='polls',_('polls')
 

class LanguageEnum(TextChoices):
    FARSI="فارسی",_("فارسی")
    ENGLISH="انگلیسی",_("انگلیسی")
    
def LanguageCode(language):
    if language==LanguageEnum.FARSI:
        return 'fa'
    if language==LanguageEnum.ENGLISH:
        return 'en'
def LanguageFromCode(code):
    if code=='fa':
        return LanguageEnum.FARSI
    if code=='en':
        return LanguageEnum.ENGLISH
   
class PictureNameEnum(TextChoices):
    LOGO="لوگو",_("لوگو")
    FAVICON="آیکون",_("آیکون")
    BACKGROUND="پس زمینه",_("پس زمینه")
    APP_BACKGROUND_IMAGE="تصویر پس زمینه اپ",_("تصویر پس زمینه اپ")
    
class ColorEnum(TextChoices):
    SUCCESS = 'success', _('success')
    DANGER = 'danger', _('danger')
    WARNING = 'warning', _('warning')
    PRIMARY = 'primary', _('primary')
    MUTED = 'muted', _('muted')
    SECONDARY = 'secondary', _('secondary')
    INFO = 'info', _('info')
    LIGHT = 'light', _('light')
    ROSE = 'rose', _('rose')
    DARK = 'dark', _('dark') 





def class_title(*args, **kwargs):
    class_name='page'
    app_name='core'
    if 'class_name' in kwargs:
        class_name=kwargs['class_name']
    if 'app_name' in kwargs:
        app_name=kwargs['app_name']

    class_title = "صفحه"

 

    if class_name == "maintenanceinvoice":
        class_title = "فاکتور تعمیر و نگهداری"
    if class_name == "exam":
        class_title = "آزمون"
    if class_name == "pricingpage":
        class_title = "لیست قیمت"
    if class_name == "drug":
        class_title = "دارو"
    if class_name == "poll":
        class_title = "پرسش"
    if class_name == "account":
        class_title = "حساب"
    if class_name == "course":
        class_title = "واحد درسی"
    if class_name == "payment":
        class_title = "پرداخت"
    if class_name == "prescription":
        class_title = "نسخه"
    if class_name == "property":
        class_title = "ملک"
    if class_name == "book":
        class_title = "کتاب"
    if class_name == "personaccount":
        class_title = "حساب شخصی"
    if class_name == "page":
        class_title = "صفحه"
    if class_name == "appointment":
        class_title = "قرار ملاقات"
    if class_name == "coupon":
        class_title = "جایزه خرید"
    if class_name == "letter":
        class_title = "نامه"
    if class_name == "file":
        class_title = "فایل"
    if class_name == "ourwork":
        class_title = "پروژه"
    if class_name == "feature":
        class_title = "خدمات"
    if class_name == "blog":
        class_title = "مقاله"
    if class_name == "material":
        class_title = "متریال"
    if class_name == "product":
        class_title = "کالا"
    if class_name == "vehicle":
        class_title = "وسیله نقلیه"
    if class_name == "project":
        class_title = "پروژه"
    if class_name == "cost":
        class_title = "هزینه"
    if class_name == "service":
        class_title = "سرویس"
    if class_name=="pm_service":
        class_title = "سرویس"
    if class_name=="luggage":
        class_title = "محموله بار"
    if class_name == "organizationalunit":
        class_title = "واحد سازمانی"
    if class_name == "event":
        class_title = "رویداد"
    if class_name=="invoice":
        class_title= "فاکتور"
    if class_name=="maintenance":
        class_title= "تعمیر و نگهداری"
    if class_name=="materialinvoice":
        class_title= "فاکتور متریال"
    if class_name=="serviceinvoice":
        class_title ="فاکتور خدمات"
    if class_name=="workshift":
        class_title= "شیفت کاری"
    if class_name=="fooditem":
        class_title= "آیتم غذایی"
    if class_name=="role":
        class_title= "نقش"
    if class_name=="financialdocument":
        class_title= "سند مالی"
    if class_name=="financialevent":
        class_title= "رویداد مالی"
    return class_title
class ParameterNameEnum(TextChoices):
    VISITOR_COUNTER="تعداد بازدید",_("تعداد بازدید")
    CURRENCY="واحد پول",_("واحد پول")
    TITLE="عنوان",_("عنوان")
    FARSI_FONT_NAME="نام فونت فارسی",_("نام فونت فارسی")
    HOME_URL="لینک به خانه",_("لینک به خانه")
    THUMBNAIL_DIMENSION="عرض تصاویر کوچک",_("عرض تصاویر کوچک")
    SHOW_ARCHIVES="نمایش فایل های آرشیو شده",_("نمایش فایل های آرشیو شده")
    HAS_APP_BACKGROUND="اپ تصویر زمینه دارد؟",_("اپ تصویر زمینه دارد؟")