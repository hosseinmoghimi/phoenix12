from django import template
from phoenix.server_settings import CURRENCY
from utility.currency import to_price
register = template.Library()
@register.filter
def to_price_color_btn(vall):
    color="primary" 
    if vall>0:
        color="success" 
    if vall<0:
        color="danger" 
    return f"""
    <btn @click="copy_balance()" class="btn btn-{color}" >{to_price(vall)} </btn>
    """