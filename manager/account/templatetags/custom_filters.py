from django import template
from django.utils.dateformat import DateFormat

register = template.Library()

@register.filter
def format_datetime(value):
    if not value:
        return
    df = DateFormat(value)
    formatted_date = df.format('d.m.Y H:i')
    return formatted_date

@register.filter
def format_date(value):
    return value.strftime('%d.%m.%Y')

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def add(value, arg):
    return value + arg