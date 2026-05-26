from django import template
register = template.Library()

@register.filter
def to_transaction_side(financial_document):
    text="بستانکار"
    color="success"
    if financial_document.bedehkar>0:
        text="بدهکار"
        color="danger"
    return f"""<span class="badge badge-{color}">{text}</span>"""