from phoenix.server_settings import CURRENCY
from django import template
from utility.constants import TUMAN,RIAL
register = template.Library()
from utility.currency import separate as separate_origin,to_price as to_price_origin,separate as separate_origin
from utility.num import to_horuf as to_horuf_num,to_tartib as to_tartib_
from utility.log import leolog

@register.filter
def separate(value,*args, **kwargs):
    return separate_origin(value=value)


@register.filter
def to_price(value,*args, **kwargs):
    
    return to_price_origin(value=value)
@register.filter
def to_price_color(value,*args, **kwargs):
    try:
        value=int(value)
    except:
        return f"""مبلغ اشتباه """
    if value>0:
        color="success"
    if value<0:
        color="danger"
    if value==0:
        color="primary"
    return f"""
    <span class="text-{color}">{to_price_origin(value=value,color=True,*args, **kwargs)}</span>
    """
 
@register.filter
def to_price_color_or_blank(value,*args, **kwargs):
    try:
        value=int(value)
    except:
        return f"""مبلغ اشتباه """
    if value>0:
        color="success"
    if value<0:
        color="danger"
    if value==0:
        return "&nbsp"
    return f"""
    <span class="text-{color}">{to_price_origin(value=value,color=True,*args, **kwargs)}</span>
    """
 
@register.filter
def to_price_or_blank(value,*args, **kwargs):
    try:
        value=int(value)
    except:
        return f"""مبلغ اشتباه """
    if value>0:
        color="success"
    if value<0:
        color="danger"
    if value==0:
        return "&nbsp"
    return f"""
    <span class=" ">{to_price_origin(value=value,color=True,*args, **kwargs)}</span>
    """
 

@register.filter
def to_price_color_btn(value,*args, **kwargs):
    try:
        value=int(value)
    except:
        return f"""مبلغ اشتباه """
    if value>0:
        color="success"
    if value<0:
        color="danger"
    if value==0:
        return "&nbsp"
    return f"""
    <span class="btn btn-{color}">{to_price_origin(value=value,color=True,*args, **kwargs)}</span>
    """
 
@register.filter
def to_price_rial(value,*args, **kwargs):
    if CURRENCY==TUMAN:
        value=value*1
    return to_price_origin(value=value,unit=RIAL) 

 
@register.filter
def to_price_tuman(value):
    if CURRENCY==RIAL:
        value=value/10
    return to_price_origin(value=value,unit=TUMAN) 


@register.filter
def to_horuf(value):
    try:
        value=int(value)
    except:
        return f"""مبلغ اشتباه """
    return to_horuf_num(value=value)

@register.filter
def to_horuf_tuman(value):
    if CURRENCY==RIAL:
        value=value/10
    return to_horuf_num(value=value)


@register.filter
def to_horuf_rial(value):
    if CURRENCY==TUMAN:
        value=value*10
    return to_horuf_num(value=value)






@register.filter
def to_price_pure(value,*args, **kwargs):
    try:
        value=int(value)
    except:
        return f"""مبلغ اشتباه """
    return separate_origin(value,*args, **kwargs)

@register.filter
def separate(value,*args, **kwargs):
    return separate_origin(value,*args, **kwargs) 
    
@register.filter
def to_price_pure_rial(value):
    if CURRENCY==TUMAN:
        value=value*10
    return to_price_pure(value=value)
    





 
 


@register.filter
def to_tartib(value):
    return to_tartib_(value)


def separate(value):
    try:
        value=int(value)
    except:
        return ""

    if value<0:
        return '-'+separate(value=0-value)
    
    if value<1000:
        return str(value)
    else:
        return separate(value/1000)+','+str(value)[-3:]
