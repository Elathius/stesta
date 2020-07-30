import datetime
from django import template

register = template.Library()


@register.filter
def split_timeuntil(duration):
    return duration.split(",")[0]