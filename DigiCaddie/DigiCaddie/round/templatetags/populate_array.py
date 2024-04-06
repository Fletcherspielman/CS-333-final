from django import template

register = template.Library()

# To be used for adding values to an array directly from Html files

@register.simple_tag
def populate_array(existing_array, value_to_append):
    my_array = existing_array.copy() if existing_array else []
    my_array.append(value_to_append)
    return my_array