# -*- coding: utf-8 -*-
from django import template
from examples.models import Category
from accounts.models import User

register = template.Library()

@register.inclusion_tag('_menu.html', takes_context=True)
def menu(context):
    context['example_categories'] = Category.objects.all()
    return context

@register.inclusion_tag('main/_user_counter.html')
def user_counter():
    return {
        'user_count': User.objects.count()
    }