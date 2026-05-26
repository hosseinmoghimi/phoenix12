
from django import template
register = template.Library() 
from accounting.constants import ACCOUNT_CODE_SEPERATOR

CODE_SEPERATOR=ACCOUNT_CODE_SEPERATOR

def rest_code(code):
    if len(code)<3:
        return code
    return code[:2]+CODE_SEPERATOR+rest_code(code[2:])
     
@register.filter
def account_code_seperator(code):
    if len(code)<4:
        return code
    return code[:3]+CODE_SEPERATOR+rest_code(code[3:])
     