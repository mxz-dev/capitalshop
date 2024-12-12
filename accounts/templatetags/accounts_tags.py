from django import template

register = template.Library()

@register.filter()
def splitter(value, c):
    v = str(value)
    return v[-c:]