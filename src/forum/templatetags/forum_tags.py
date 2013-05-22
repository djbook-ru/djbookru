from django import template
from django.core.cache import cache
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()


@register.filter
def online(user):
    return cache.get(str(user.id))


@register.filter
def can_edit(obj, user):
    return obj.can_edit(user)


@register.filter
def can_delete(obj, user):
    return obj.can_delete(user)


@register.filter
def has_access(obj, user):
    return obj.has_access(user)


@register.filter
def has_unread(obj, user):
    return obj.has_unread(user)


@register.filter
@stringfilter
def softwraphtml(value, max_line_length=24):
    import re
    whitespace_re = re.compile('\s')
    new_value = []
    unbroken_chars = 0
    in_tag = False
    in_xhtml_entity = False
    value = escape(value)
    for idx, char in enumerate(value):
        if char == '<':
            in_tag = True
        elif char == '>':
            in_tag = False
            unbroken_chars = 0
        elif char == '&' and not in_tag:
            in_xhtml_entity = True
        elif char == ';' and in_xhtml_entity:
            in_xhtml_entity = False
        elif whitespace_re.match(char):
            unbroken_chars = 0

        new_value.append(char)
        if not in_xhtml_entity:
            if unbroken_chars >= max_line_length-1 and not in_tag:
                new_value.append("<wbr/>")
                unbroken_chars = 0
            else:
                unbroken_chars += 1
    return mark_safe(''.join(new_value))