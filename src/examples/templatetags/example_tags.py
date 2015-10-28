# -*- coding: utf-8 -*-
from django import template
from src.examples.models import Category

register = template.Library()


@register.inclusion_tag('examples/_examples_menu.html')
def examples_menu():
    return {
        'categories': Category.objects.all()
    }


@register.filter
def can_edit(obj, user):
    return obj.can_edit(user)
