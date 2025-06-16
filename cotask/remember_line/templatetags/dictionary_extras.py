import django.template

register = django.template.Library()


@register.filter
def dict_get(d, key):
    return d.get(key)
