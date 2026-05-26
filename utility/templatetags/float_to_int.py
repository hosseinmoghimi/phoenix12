
from django import template
register = template.Library() 


@register.filter
def float_to_int(value):
    int_value=int(value)
    if value-int_value==0:
        return int_value
    return value
