
from django import template
register = template.Library() 
from accounting.constants import ACCOUNT_CODE_SEPERATOR

CODE_SEPERATOR=ACCOUNT_CODE_SEPERATOR

def rest_code(code):
    if len(code)<3:
        return code
    return code[:2]+f"""<span class="text-success">{CODE_SEPERATOR}</span>"""+rest_code(code[2:])
     
@register.filter
def account_code_seperator(code):
    if len(code)<4:
        return code
    return code[:3]+f"""<span class="text-success">{CODE_SEPERATOR}</span>"""+rest_code(code[3:])  

def rest_card_no(card_no):
    if len(card_no)<5:
        return card_no
    return card_no[:4]+f"""<span class="text-success">{CODE_SEPERATOR}</span>"""+rest_card_no(card_no[4:])
    # return rest_card_no(card_no[4:])+f"""<span class="text-success">{CODE_SEPERATOR}</span>"""+card_no[:4]
     
@register.filter
def card_no_seperator(card_no):
    if len(card_no)<5:
        return card_no
    return card_no[:4]+f"""<span class="text-success">{CODE_SEPERATOR}</span>"""+rest_card_no(card_no[4:])
    # return rest_card_no(card_no[4:])+f"""<span class="text-success">{CODE_SEPERATOR}</span>"""+card_no[:4]