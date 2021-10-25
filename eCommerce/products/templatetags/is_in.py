from django import template

register = template.Library()


@register.filter(name='is_in')
def is_in(value, arg):
    return value in arg
