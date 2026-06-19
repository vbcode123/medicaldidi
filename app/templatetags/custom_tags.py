from django import template

register = template.Library()

@register.filter(name='split')
def split_string(value, arg):
    return value.split(arg)
