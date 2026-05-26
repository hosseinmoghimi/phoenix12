from django import template
register = template.Library()
@register.filter
def to_variz_text(bank_account):
    # return bank_account.to_variz_text() 
    return "to_variz_text template tag"