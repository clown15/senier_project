from django import template

register = template.Library()

@register.filter
def get_item(dict,key):
    if key in dict:
        return dict[key]
    else:
        return None