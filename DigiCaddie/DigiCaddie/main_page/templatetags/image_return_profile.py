
from django import template

register = template.Library()

@register.simple_tag
def image_return_profiles(index, sec, rows_cols):
    return rows_cols[index][sec].picture.url

@register.simple_tag
def image_return_profiles_id(index, sec, rows_cols):
    return rows_cols[index][sec].id

@register.simple_tag
def image_return_counter(index, mult):
    return index * mult   