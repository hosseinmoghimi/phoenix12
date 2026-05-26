from .constants import TUMAN,RIAL
from phoenix.server_settings import CURRENCY
from utility.templatetags.to_amount_color import to_amount_color
def to_price_colored(price):
    return f"""<span class="text-{to_amount_color(price)}">{to_price(price)}</span>"""


def to_price(value,unit=CURRENCY,*args, **kwargs):
    # from core.repo import Parameter,ParameterNameEnum
    # (parameter,i)=Parameter.objects.get_or_create(name=ParameterNameEnum.CURRENCY)
    # unit=parameter.value
    # CURRENCY=parameter.value
    if unit==TUMAN:
        pass
    if unit==RIAL and CURRENCY==TUMAN:
        value=value*10
    """converts int to string"""  
    try:
        value=int(value)
        sign=''
        if value<0:
            value=0-value
            sign='- '
        a=separate(value)
        stringed_number= sign+a #+' '+unit
    except:
        stringed_number= " مقدار عددی نامعتبر"
    if 'color' in kwargs and value<0:
        return f"""
            <span class="danger">{stringed_number}<span>
        """
    return stringed_number

def separate(price):
    
    try:
        price=int(price)
    except:
        return None
    
    if price<1000:
        return str(price)
    else:
        return separate(price/1000)+','+str(price)[-3:]
