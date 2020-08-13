from django import template


register = template.Library()

@register.filter()
def clean(value):
    return value.replace('_', ' ')
