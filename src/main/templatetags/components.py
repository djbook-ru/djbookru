# -*- coding: utf-8 -*-
from django import template
from examples.models import Category

register = template.Library()

@register.inclusion_tag('_menu.html', takes_context=True)
def menu(context):
    context['example_categories'] = Category.objects.all()
    return context