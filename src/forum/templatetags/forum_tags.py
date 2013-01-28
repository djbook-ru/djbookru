from django import template
from django.core.cache import cache

register = template.Library()


@register.filter
def online(user):
    return cache.get(str(user.id))