from django import template
register = template.Library()
from phoenix.server_settings import FULL_SITE_URL
@register.filter
def to_absolute_link(url):
    absolute_link=""
    if FULL_SITE_URL[len(FULL_SITE_URL)-1]=="/" and url[0]=="/":
        absolute_link=FULL_SITE_URL[0:len(FULL_SITE_URL)-1]+url
    else:
        absolute_link=FULL_SITE_URL+url
    if absolute_link[len(absolute_link)-1]=="/":
        pass
    else:
        absolute_link=absolute_link+"/"
    return absolute_link