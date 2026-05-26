
from django import template
register = template.Library()
from django.utils.translation import gettext as _
@register.filter
def to_text_color(vall):
     
    if vall is None:
        return 'muted'
    if vall=="ورود" or vall=="وارد" or vall==_("ورود") or vall==_("وارد"):
        return 'success'
    if vall=="خروج"or vall=="خارج" or vall==_("خروج") or vall==_("خارج"):
        return 'danger'