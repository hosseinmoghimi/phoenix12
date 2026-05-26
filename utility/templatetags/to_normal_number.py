
from django import template
register = template.Library()

@register.filter
def to_normal_number(value,*args, **kwargs):
    a=format(value, '.2f') 
    s=str(a)
    if value-int(value)==0:
        s=str(int(value))
    # if s[len(s)-3:]==".00":
    #     s=s[:len(s)-3]
    return s