from django import template

register = template.Library()

@register.filter
def img_filter(value):
    return value.replace('dashboard/static/', 'static/') 