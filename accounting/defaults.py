from .models import Account
from utility.constants import SUCCEED,FAILED
 
DEFAULT_PRIORITY=1000
def default_accounts():

    account_groups=[
        
        {'code':"1","name":"دارایی جاری",'color':'success','priority':DEFAULT_PRIORITY},
        {'code':"2" ,"name":"دارایی های غیر جاری",'color':'primary','priority':DEFAULT_PRIORITY},
        {'code':"3","name":"بدهی های جاری	",'color':'danger','priority':DEFAULT_PRIORITY },
        {'code':"4" ,"name":"بدهی های بلند مدت (غیرجاری)",'color':'success','priority':DEFAULT_PRIORITY },
        {'code':"5","name":"حقوق صاحبان سهام",'color':'success','priority':DEFAULT_PRIORITY },  
        {'code':"6","name":"درآمد ها",'color':'info','priority':DEFAULT_PRIORITY },
        {'code':"7","name":"بهای تمام شده کالای فروش رفته و خدمات ارائه شده",'color':'primary','priority':DEFAULT_PRIORITY },
        {'code':"8","name":"هزینه ها",'color':'danger', 'priority':DEFAULT_PRIORITY},
        {'code':"9","name":"سایر حسابها",'color':'success','priority':DEFAULT_PRIORITY },
        
    ]   

    basic_accounts=[
            #111111111111111111111111111
            {'code':"101","name":"موجودی نقد و بانک",'priority':DEFAULT_PRIORITY,'parent_code':"1",'color':'success' },
            {'code':"102","name":"سرمایه گذاری کوتاه مدت",'priority':DEFAULT_PRIORITY,'parent_code':"1",'color':'warning'},
            {'code':"103","name":"حساب ها و اسناد دریافتنی تجاری",'priority':DEFAULT_PRIORITY,'parent_code':"1",'color':'success'},
            {'code':"104","name":"سایر حساب های دریافتنی تجاری",'priority':DEFAULT_PRIORITY,'parent_code':"1",'color':'primary'},
            {'code':"105","name":"موجودی مواد و کالا",'priority':DEFAULT_PRIORITY,'parent_code':"1",'color':'success'},
            {'code':"106","name":"جاری شرکا",'priority':DEFAULT_PRIORITY,'parent_code':"1",'color':'success'},
            {'code':"107","name":"سفارشات و پیش پرداختها",'priority':DEFAULT_PRIORITY,'parent_code':"1",'color':'success'},
            {'code':"108","name":"سپرده هایمان نزد دیگران",'priority':DEFAULT_PRIORITY,'parent_code':"1",'color':'success'},
            {'code':"109","name":"دارایی های نگهداری شده برای فروش",'priority':DEFAULT_PRIORITY,'parent_code':"1",'color':'success'},
            #222222222222222222222222
            {'code':"201","name":"دارایی های ثابت مشهود",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"2"}, 
            {'code':"202","name":"استهلاک انباشته دارایی های ثابت مشهود",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"2" }, 
            {'code':"203","name":"دارایی های در جریان تکمیل",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"2"}, 
            {'code':"204","name":"دارایی های نامشهود",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"2"}, 
            {'code':"205","name":"سرمایه گذاری های بلند مدت",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"2" },  
            #3333333333333333333333333
            {'code':"301","name":"ﺣﺴﺎب ﻫﺎ و اﺳﻨﺎد ﭘﺮداﺧﺘﻨﯽ ﺗﺠﺎری",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"3"},  
            {'code':"302","name":"ﺳﺎﯾﺮ ﺣﺴﺎب ﻫﺎ و اﺳﻨﺎد ﭘﺮداﺧﺘﻨﯽ",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"3"},  
            {'code':"303","name":"ﺳﻔﺎرﺷﺎت و ﭘﯿﺶ درﯾﺎﻓﺖ ﻫﺎ",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"3"},  
            {'code':"304","name":"ذﺧﯿﺮه ﻣﺎﻟﯿﺎت",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"3"},  
            {'code':"305","name":"ﺳﻮد ﺳﻬﺎم ﭘﺮداﺧﺘﻨﯽ",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"3"},  
            {'code':"306","name":"ﺳﭙﺮده ﻫﺎی ﭘﺮداﺧﺘﻨﯽ",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"3"},  
            {'code':"307","name":"ﺗﺴﻬﯿﻼت و اﻋﺘﺒﺎرات ﻣﺎﻟﯽ درﯾﺎﻓﺘﯽ ﮐﻮﺗﺎه ﻣﺪت",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"3" },  
            {'code':"308","name":"ذﺧﺎﯾﺮ",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"3" },  
            #4444444444444444444444444
            {'code':"401","name":"ﺣﺴﺎب ﻫﺎ و اﺳﻨﺎد ﭘﺮداﺧﺘﻨﯽ ﺑﻠﻨﺪ ﻣﺪت ﺗﺠﺎری",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"4" },  
            {'code':"402","name":"ﺳﺎﯾﺮ ﺣﺴﺎب ﻫﺎ و اﺳﻨﺎد ﭘﺮداﺧﺘﻨﯽ ﺑﻠﻨﺪﻣﺪت",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"4" },  
            {'code':"403","name":"ﺗﺴﻬﯿﻼت و اﻋﺘﺒﺎرات ﻣﺎﻟﯽ درﯾﺎﻓﺘﯽ ﺑﻠﻨﺪﻣﺪت",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"4" },  
            {'code':"404","name":"ذﺧﯿﺮه ﻣﺰاﯾﺎی ﭘﺎﯾﺎن ﺧﺪﻣﺖ ﮐﺎرﮐﻨﺎن",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"4" },  
            {'code':"405","name":"درآﻣﺪﻫﺎی اﻧﺘﻘﺎﻟﯽ ﺑﻪ دوره ﻫﺎی آﺗﯽ",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"4" },  
            #5555555555555555555555555
            {'code':"501","name":"ﺳﺮﻣﺎﯾﻪ ﭘﺮداﺧﺖ ﺷﺪه",'color':'info','priority':DEFAULT_PRIORITY,'parent_code':"5" },  
            {'code':"502","name":"اﻧﺪوﺧﺘﻪ ﻗﺎﻧﻮﻧﯽ",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"5" },  
            {'code':"503","name":"ﺳﺎﯾﺮ اﻧﺪوﺧﺘﻪ ﻫﺎ",'color':'info','priority':DEFAULT_PRIORITY,'parent_code':"5" },  
            {'code':"504","name":"ﻣﺎزاد ﺗﺠﺪﯾﺪ ارزﯾﺎﺑﯽ داراﯾﯽ ﻫﺎی ﺛﺎﺑﺖ ﻣﺸﻬﻮد",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"5" },  
            {'code':"505","name":"سود ( زیان ) انباشته",'color':'info','priority':DEFAULT_PRIORITY,'parent_code':"5" },  
            #6666666666666666666666666
            {'code':"601","name":"فروش", 'color':'info','priority':DEFAULT_PRIORITY,'parent_code':"6" },  
            {'code':"602","name":"درآﻣﺪ ﺣﺎﺻﻞ از اراﺋﻪ ﺧﺪﻣﺎت",'color':'info','priority':DEFAULT_PRIORITY,'parent_code':"6" },  
            {'code':"603","name":"ﺳﺎﯾﺮ درآﻣﺪﻫﺎی ﻋﻤﻠﯿﺎﺗﯽ",'color':'info','priority':DEFAULT_PRIORITY,'parent_code':"6" },  
            {'code':"604","name":"ﺳﺎﯾﺮ درآﻣﺪﻫﺎی ﻏﯿﺮ ﻋﻤﻠﯿﺎﺗﯽ",'color':'info','priority':DEFAULT_PRIORITY,'parent_code':"6" },  
            #777777777777777777777777
            {'code':"701","name":"ﺑﻬﺎی ﺗﻤﺎم ﺷﺪه ﮐﺎﻻی ﻓﺮوش رﻓﺘﻪ داﺧﻠﯽ",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"7" },  
            {'code':"702","name":"ﺑﻬﺎی ﺗﻤﺎم ﺷﺪه ﮐﺎﻻی ﻓﺮوش رﻓﺘﻪ ﺧﺎرﺟﯽ",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"7" },  
            {'code':"703","name":"ﺑﻬﺎی ﺗﻤﺎم ﺷﺪه ﺧﺪﻣﺎت اراﺋﻪ ﺷﺪه",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"7" },  
            #888888888888888888888888
            {'code':"801","name":"هزﯾﻨﻪ ﺣﻘﻮق و دﺳﺘﻤﺰد ﮐﺎرﮐﻨﺎن ﻏﯿﺮ ﺗﻮﻟﯿﺪی",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"8" },  
            {'code':"802","name":"هزﯾﻨﻪ ﻫﺎی ﻋﻤﻠﯿﺎﺗﯽ",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"8" },  
            {'code':"803","name":"سایر هزﯾﻨﻪ ﻫﺎی ﻋﻤﻠﯿﺎﺗﯽ",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"8" },  
            {'code':"804","name":"هزینه ﻫﺎی ﻣﺎﻟﯽ",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"8" },  
            {'code':"805","name":"هزینه ﻫﺎی ﻏﯿﺮ ﻋﻤﻠﯿﺎﺗﯽ",'color':'danger','priority':DEFAULT_PRIORITY,'parent_code':"8" },  
            #999999999999999999999999
            {'code':"901","name":"ﺣﺴﺎب ﻫﺎی اﻧﺘﻈﺎﻣﯽ",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"9" },  
            {'code':"902","name":"طرف ﺣﺴﺎب ﻫﺎی اﻧﺘﻈﺎﻣﯽ",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"9" },  
            {'code':"903","name":"ﺗﺮاز اﻓﺘﺘﺎﺣیه",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"9" },  
            {'code':"904","name":"ﺗﺮاز اختتامیه",'color':'secondary','priority':DEFAULT_PRIORITY,'parent_code':"9" },  

    ]  
    moein_accounts=[
            #101
            {'code':"10101","name":"صندوق",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"101" },
            {'code':"10102","name":"بانک",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"101" },
            {'code':"10103","name":"تنخواه",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"101" },
            {'code':"10104","name":"وجوه در راه",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"101" },
            
            
            #102
            {'code':"10201","name":"سهام شرکتهای پذیرفته شده در بورس",'color':'warning','priority':DEFAULT_PRIORITY,'parent_code':"102" },
            {'code':"10202","name":"اوراق مشارکت",'color':'warning','priority':DEFAULT_PRIORITY,'parent_code':"102" },
            {'code':"10203","name":"سرمایه گذاری در سهام شرکتها",'color':'warning','priority':DEFAULT_PRIORITY,'parent_code':"102" },
            {'code':"10204","name":"سپرده های سرمایه گذاری کوتاه مدت",'color':'warning','priority':DEFAULT_PRIORITY,'parent_code':"102" },
            #103
            {'code':"10301","name":"اسناد دریافتنی تجاری / شرکت ها",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"103" },
            {'code':"10302","name":"اسناد دریافتنی تجاری / اشخاص",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"103" },
            {'code':"10303","name":"حسابهای دریافتنی تجاری / شرکت ها",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"103" },
            {'code':"10304","name":"حسابهای دریافتنی تجاری / اشخاص",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"103" },
            #104
            {'code':"10401","name":"کارکنان ( وام مساعده )",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"104" },
            {'code':"10402","name":"اسناد دریافتنی",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"104" },
            {'code':"10403","name":"سپرده های موقت",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"104" },
            {'code':"10404","name":"سود سهام دریافتنی",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"104" },
            {'code':"10405","name":"طلب از شرکت گروهها",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"104" },
            {'code':"10406","name":"طلب از سایر اشخاص وابسته",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"104" },
            {'code':"10407","name":"سایر اشخاص",'color':'primary','priority':DEFAULT_PRIORITY,'parent_code':"104" },
            #105
            {'code':"10501","name":"کالای ساخته شده",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"105" },
            {'code':"10502","name":"کالای در جریان ساخت",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"105" },
            {'code':"10503","name":"مواد اولیه و بسته بندی",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"105" },
            {'code':"10504","name":"قطعات و لوازم یدکی",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"105" },
            {'code':"10505","name":"سایر موجودی ها",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"105" },
            {'code':"10506","name":"کالای در راه",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"105" },
            #106
            #107

            #201
            {'code':"201/01","name":"زمین",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            {'code':"201/02","name":"ساختمان",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            {'code':"201/03","name":"تاسیسات",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            {'code':"201/04","name":"ماشین آلات و تجهیزات ",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            {'code':"201/05","name":"اثاثه و منصوبات",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            {'code':"201/06","name":"ابزار آلات",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            {'code':"201/07","name":"وسایل نقلیه",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            {'code':"201/08","name":"دارایی ها در دست تکمیل",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            {'code':"201/09","name":"سفارشات و پیش پرداخت های سرمایه ای ",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            {'code':"201/10","name":"اقلام سرمایه ای در انبار",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"201" },
            #204
            {'code':"20401","name":"حق امتیاز استفاده از خدمات عمومی",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"204" },
            {'code':"20402","name":"سرقفلی محل کسب",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"204" },
            {'code':"20403","name":"سایر داراییهای نا مشهود",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"204" },

            #205



            #501
            {'code':"50101","name":"سرمایه",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"501" }, 

    ]


    ################################    301
    color ="danger"
    parent_code="301"
    moein_accounts.append({'code':"30101","name":"اسناد پرداختنی تجاری/شرکتهای گروه",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30102","name":"اسناد پرداختنی تجاری/سایر اشخاص وابسته",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30103","name":"اسناد پرداختنی تجاری/سایر اشخاص",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30104","name":"حسابهای پرداختنی تجاری/شرکتهای گروه",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30105","name":"حسابهای پرداختنی تجاری/سایر اشخاص وابسته",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30106","name":"حسابهای پرداختنی تجاری/سایر اشخاص",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
  

    #################################    302
    color ="secondary"
    parent_code="302"
    moein_accounts.append({'code':"30201","name":"اسناد پرداختنی غیر تجاری",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30202","name":"شرکتهای گروه",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30203","name":"سایر اشخاص وابسته",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30204","name":"مالیاتهای تکلیفی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30205","name":"حق بیمه های پرداختنی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30206","name":"سپرده حسن انجام کار",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30207","name":"ذخیره هزینه های تعلق گرفته پرداخت نشده",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30208","name":"متفرقه (سایر)",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )

    ##################################    303
    color ="primary"
    parent_code="303"
    moein_accounts.append({'code':"30301","name":"پیش دریافت از مشتری",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30302","name":"شرکتهای گروه",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30303","name":"سایر اشخاص وابسته",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30304","name":"سایر مشتریان",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30305","name":"سایر پیش دریافتها",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )


    #################################    304
    color ="success"
    parent_code="304"
    moein_accounts.append({'code':"30401","name":"به تفکیک دوره",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
  

    #################################    305
    color ="success"
    parent_code="305"
    moein_accounts.append({'code':"30501","name":"سود سهام پیشنهادی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30502","name":"سود سهام پرداختنی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
  
    #################################    307
    color ="success"
    parent_code="307"
    moein_accounts.append({'code':"30701","name":"بانکها",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30702","name":"شرکتهای گروه",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30703","name":"سایر اشخاص وابسته",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30704","name":"سایر اشخاص",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30705","name":"حصه بلند مدت",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"30706","name":"حصه جاری",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
  


    #################################    402
    color ="success"
    parent_code="402"
    moein_accounts.append({'code':"40201","name":"اسناد پرداختنی ارزی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40202","name":"اسناد پرداختنی ریالی/واگذاری به وزارت امور اقتصادی و دارایی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40203","name":" اسناد پرداختنی ریالی/واگذاری به تامین اجتماعی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40204","name":"اسناد پرداختنی ریالی/سایر اسناد پرداختنی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40205","name":"حسابهای پرداختنی/تجاری ",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40206","name":"حسابهای پرداختنی/شرکتهای گروه",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40207","name":"حسابهای پرداختنی/سایر اشخاص وابسته",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
  

    #################################    403
    color ="secondary"
    parent_code="403"
    moein_accounts.append({'code':"40301","name":"بانکها",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40302","name":"شرکتهای گروه",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40303","name":"سایر اشخاص وابسته",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40304","name":"سایر اشخاص",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40305","name":"حصه بلند مدت",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"40306","name":"حصه جاری",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
  

    #################################    701
    color ="secondary"
    parent_code="701"
    moein_accounts.append({'code':"70101","name":"مواد مستقیم مصرفی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70102","name":"دستمزد مستقیم",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70103","name":"سربار تولید",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70104","name":"هزینه های جذب نشده در تولید",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70105","name":"موجودی کالای در جریان ساخت",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70106","name":"ضایعات غیر عادی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70107","name":"موجودی کالای ساخته شده",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
  


    #################################    702
    color ="primary"
    parent_code="702"
    moein_accounts.append({'code':"70201","name":"مواد مستقیم مصرفی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70202","name":"دستمزد مستقیم",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70203","name":"سربار تولید",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70204","name":"هزینه های جذب نشده در تولید",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70205","name":"موجودی کالای در جریان ساخت",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70206","name":"ضایعات غیر عادی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70207","name":"موجودی کالای ساخته شده",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
  


    #################################    703
    color ="secondary"
    parent_code="703"
    moein_accounts.append({'code':"70301","name":"مواد مستقیم مصرفی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70302","name":"دستمزد مستقیم",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70303","name":"سربار تولید",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70304","name":"هزینه های جذب نشده در تولید",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70305","name":"موجودی کالای در جریان ساخت",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70306","name":"ضایعات غیر عادی",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
    moein_accounts.append({'code':"70307","name":"موجودی کالای ساخته شده",'color':color,'priority':DEFAULT_PRIORITY,'parent_code':parent_code }, )
  

    moein2_accounts=[
            {"name":"صندوق فروشگاه",'code':"1010101",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"10101" },
            {"name":"صندوق دفتر",'code':"1010102",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"10101" },

            {"name":"بانک ملی",'code':"1010201",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"10102" },
            {"name":"بانک رفاه",'code':"1010202",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"10102" },
            {"name":"بانک ملت",'code':"1010203",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"10102" },
            {"name":"بانک تجارت",'code':"1010204",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"10102" },

            
            #50101
            {'code':"5010101","name":"نقدی",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"50101" },
            {'code':"5010102","name":"تعهد شده",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"50101" },
    ]
    tafsili_accounts=[
            {"name":"صندوق بی ضرر",'code':"101010101",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"1010101" },
            {"name":"صندوق درست",'code':"101010102",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"1010101" },
            {"name":"صندوق شرباف",'code':"101010201",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"1010102" },
            {"name":"صندوق معتبر",'code':"101010202",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"1010102" },

            {"name":"بانک ملی به شماره 0101581354009",'code':"0101581354009",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"1010201" },

            {"name":"حسین مقیمی نقدی",'code':"501010101",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"5010101" },
            {"name":"داوود قانع نقدی",'code':"501010102",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"5010101" },
            {"name":"حسین مقیمی تعهد شده",'code':"501010201",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"5010102" },
            {"name":"داوود قانع تعهد شده",'code':"501010202",'color':'success','priority':DEFAULT_PRIORITY,'parent_code':"5010102" },

    ]

    accounts=[]
    for account in account_groups:
        accounts.append(account)

        
    for account in basic_accounts:
        accounts.append(account)

        
    for account in moein_accounts:
        accounts.append(account)

        
    for account in moein2_accounts:
        accounts.append(account)

        
    for account in tafsili_accounts:
        accounts.append(account)
    return accounts

    
def default_persons():
    from accounting.enums import PersonCategoryEnum
    person_categories=[
        {"code":"100","title":PersonCategoryEnum.PERSONNEL,"account_code":"5010101"},
        {"code":"200","title":PersonCategoryEnum.CONTRACTOR,"account_code":"501010102"},
        {"code":"300","title":PersonCategoryEnum.CUSTOMER,"account_code":"30401"},
        {"code":"400","title":PersonCategoryEnum.SUPPLIER,"account_code":"10302"},
        {"code":"500","title":PersonCategoryEnum.EMPLOYER,"account_code":"702"},
        {"code":"600","title":PersonCategoryEnum.COST,"account_code":"701"},
        {"code":"600","title":PersonCategoryEnum.DEFAULT,"account_code":"801"},
    ]
    persons=[
        {"code":"10001","first_name":"حسین","last_name":"مقیمی","melli_code":"076983545","categories":["100","200"]},
        {"code":"10002","first_name":"داوود","last_name":"قانع","melli_code":"076983543","categories":["100","200"]},
        {"code":"10003","first_name":"ابراهیم","last_name":"محمدی","melli_code":"076983541","categories":["400","600"]},
    ]
    return person_categories,persons



def default_banks():
    banks=[
        {"code":"101","name":"بانک ملی", },
        {"code":"102","name":"بانک ملت", },
        {"code":"103","name":"بانک کشاورزی", },
        {"code":"104","name":"بانک سپه", },
        {"code":"105","name":"بانک تجارت", },
        {"code":"106","name":"بانک مهر ایرانیان", },
        {"code":"107","name":"بانک پاسارگاد", },
        {"code":"108","name":"بانک سامان", },
        {"code":"109","name":"بانک صادرات", },
        {"code":"110","name":"بانک رفاه کارگران", },
      
    ]
    
    return banks