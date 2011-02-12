# -*- coding: utf-8 -*-
from django import template
from examples.models import Category
from accounts.models import User
from django.contrib.sites.models import Site
from django.template.loader import get_template
from django.template import Context
from django.conf import settings

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

@register.inclusion_tag('main/_facebook_like.html')    
def facebook_like(link):
    site = Site.objects.get_current()
    if hasattr(link, 'get_absolute_url'):
        link = link.get_absolute_url()
    return {
        'link': 'http://%s%s' % (site.domain, link) 
    }
    
class ShareNode(template.Node):
    def __init__(self, obj):
        self.obj = obj
        self.site = Site.objects.get_current()
        
    def render(self, context):
        resolved = self.obj.resolve(context)
        
        return get_template('main/_share_links.html').render(Context({
            'url': 'http://%s%s' % (self.site.domain, resolved.get_absolute_url()),
            'content': getattr(resolved, 'get_share_description', lambda: '')(),
            'title': getattr(resolved, 'get_share_title', resolved.__unicode__)(),
            'obj': resolved,
            'MEDIA_URL': settings.MEDIA_URL                                 
        }))
    
@register.tag
def get_share_links(parser, token):
    obj = token.split_contents()[1]
    
    try:
        obj = template.Variable(obj)
    except:
        raise template.TemplateSyntaxError, 'Unable to resolve %s.' % obj
    
    return ShareNode(obj)

@register.filter(name="plus_spaces")
def plus_spaces(value, *args):
    return value.replace(' ', '+').replace('%20', '+')
plus_spaces.is_safe = True
