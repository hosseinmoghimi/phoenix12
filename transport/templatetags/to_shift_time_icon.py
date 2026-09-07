from django import template
register = template.Library()
@register.filter
def to_shift_time_icon(value,*args, **kwargs):
    if value=='روز':
        return 'sun.png'
    return 'moon.png' 
