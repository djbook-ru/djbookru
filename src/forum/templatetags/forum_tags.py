from django import template
from django.core.cache import cache

register = template.Library()


@register.filter
def online(user):
    return cache.get(str(user.id))


@register.filter
def can_edit(post, user):
    return post.can_edit(user)


@register.filter
def has_access(obj, user):
    return obj.has_access(user)


@register.filter
def has_unread(obj, user):
    return obj.has_unread(user)
