yekans=['صفر',
    'یک',
    'دو',
    'سه',
    'چهار',
    'پنج',
    'شش',
    'هفت',
    'هشت',
    'نه',
    'ده',
    'یازده',
    'دوازده',
    'سیزده',
    'چهارده',
    'پانزده',
    'شانزده',
    'هفده',
    'هجده',
    'نوزده',
    'بیست',
    
    ]
dahgans=[
    '-',
    '-',
    'بیست',
    'سی',
    'چهل',
    'پنجاه',
    'شصت',
    'هفتاد',
    'هشتاد',
    'نود',
    ]
sadgans=[
    '-',
    'صد',
    'دویست',
    'سیصد',
    'چهارصد',
    'پانصد',
    'ششصد',
    'هفتصد',
    'هشتصد',
    'نهصد',
]

hezars=[
    '',
    'هزار',
    'میلیون',
    'میلیارد',
    'بیلیون',
    'بیلیارد',
    'تریلیون',
    'تریلیارد',
]
def to_horuf_3(value):
    yekan=value%10
    dahgan=int((value%100)/10)
    sadgan=int((value%1000)/100)
    if value<21:
        return yekans[value]
    if value<100:
        return dahgans[dahgan]+((' و '+ yekans[yekan] ) if yekan>0 else '')
    if value<1000:
        return  sadgans[sadgan]+((' و '+to_horuf_3(value%100)) if value%100>0 else '')

    return "error"

def to_horuf(value,hezar_power=0): 
    value=int(value)
    if value is None or value=="" :
        return "نامعتبر"
    if value==0 :
        return "صفر"
    if value<0:
        return 'منفی '+to_horuf(0-value) 
    value=int(value)
    if value<1000:
        return to_horuf_3(value)+(' '+(hezars[hezar_power]) if hezar_power>0 else '')
    else :
        return to_horuf(int(value/1000),hezar_power+1)+((' و '+to_horuf(value%1000,hezar_power)) if value%1000>0 else '')

def separate(price):
    
    try:
        price=int(price)
    except:
        return None
    
    if price<1000:
        return str(price)
    else:
        return separate(price/1000)+','+str(price)[-3:]




def to_tartib(value):
    if value<1:
        return "نامعتبر"
    if value<10:
        return (['اول',
        'دوم',
        'سوم',
        'چهارم',
        'پنجم',
        'ششم',
        'هفتم',
        'هشتم',
        'نهم',
        'دهم',
        'یازدهم',
        ])[value-1]
    return to_horuf(value-1)+"م"
    

def filter_number(s):
    i=""
    for ch in s:
        if ch=="0" or ch=="1" or ch=="2" or ch=="3" or ch=="4" or ch=="5" or ch=="6" or ch=="7" or ch=="8" or ch=="9"  :
            i+=ch
    if i=="":
        return 0
    
    return i


def fixed_length(num,length):
    str_num=str(num)
    if len(str_num)<length:
        str_num=(length-len(str_num))*"0"+str_num
    return str_num