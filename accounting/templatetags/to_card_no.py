
from django import template
register = template.Library() 
from accounting.constants import CARD_NO_SEPERATOR
   
@register.filter
def to_card_no(code):
    if len(code)<5:
        return code
    return code[:4]+CARD_NO_SEPERATOR+to_card_no(code[4:])
     