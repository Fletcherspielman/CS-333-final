from django import template

register = template.Library()

@register.simple_tag
def increment(value, arg):
    return value + arg