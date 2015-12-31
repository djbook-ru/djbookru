# -*- coding: utf-8 -*-

import markdown
import re
import datetime
from random import shuffle

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.template import Context
from django.template.defaultfilters import truncatewords_html, stringfilter, urlize, linebreaksbr
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from src.accounts.models import User
from src.comments.models import Comment
from src.doc_comments.models import Comment as DocComment
from src.examples.models import Category, Example
from src.forum.models import Topic
from src.main.forms import SearchForm, content_choices
from src.header_messages.models import HeaderMessage


RECIPES_ON_MAIN = getattr(settings, 'RECIPES_ON_MAIN', 4)
FORUM_TOPIC_ON_MAIN = getattr(settings, 'FORUM_TOPIC_ON_MAIN', 4)


register = template.Library()


@register.filter
@stringfilter
def filter_markdown(value, words=None):
    html = markdown.markdown(value)
    html = re.sub(r'<(?!\/?a(?=>|\s.*>))\/?.*?>', '', html)

    html = mark_safe(linebreaksbr(urlize(html)))

    if words:
        return truncatewords_html(html, words)

    return html


@register.inclusion_tag('_recipes.html', takes_context=True)
def recipes(context):
    context['recipe_categories'] = Category.objects.all()
    return context


@register.inclusion_tag('_menu.html', takes_context=True)
def menu(context):
    context['rnd_message'] = HeaderMessage.random_message()
    context['example_categories'] = Category.objects.all()
    return context


@register.inclusion_tag('_user_activities.html', takes_context=True)
def user_activities(context):
    context['last_forum_topics'] = Topic.objects.filter(forum__category__groups__isnull=True).order_by('-updated')
    context['last_comments'] = Comment.objects.order_by('-submit_date')
    context['last_doc_comments'] = DocComment.objects.exclude(status=DocComment.CLOSED).order_by('-created')
    return context


@register.inclusion_tag('main/_user_counter.html')
def user_counter():
    return {
        'user_count': User.objects.count()
    }


@register.assignment_tag
def is_happy_new_year():
    today = datetime.date.today()
    return today.month == 12 and today.day == 31 or today.month == 1 and today.day in range(1, 11)


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
        url = u'/'
        title = lambda: u''
        resolved = self.obj.resolve(context)
        if resolved:
            # if no book has been uploaded yet
            url = resolved.get_absolute_url()
            title = resolved.__unicode__
        return get_template('main/_share_links.html').render(Context({
            'url': 'http://%s%s' % (self.site.domain, url),
            'content': getattr(resolved, 'get_share_description', lambda: u'')(),
            'title': getattr(resolved, 'get_share_title', title)(),
            'obj': resolved,
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


@register.inclusion_tag('main/_random_recipes.html')
def random_recipes():
    ids = list(Example.objects.approved().values_list('pk', flat=True))
    shuffle(ids)
    return {
        'examples': Example.objects.filter(pk__in=ids[:RECIPES_ON_MAIN])
    }


@register.inclusion_tag('main/_random_forum_topics.html')
def random_forum_topics():
    ids = list(Topic.objects.filter(forum__category__groups__isnull=True)
               .order_by('-updated').values_list('pk', flat=True))
    shuffle(ids)
    return {
        'topics': Topic.objects.filter(pk__in=ids[:FORUM_TOPIC_ON_MAIN])
    }


@register.filter
def pretty_date(date_obj, extra_class=''):
    template = get_template("_pretty_date.html")
    context = Context({
        'date_obj': date_obj,
        'extra_class': extra_class
    })

    return template.render(context)


@register.filter
def search_model_name(result_item):
    model_pk = ContentType.objects.get_for_model(result_item.model).pk
    return dict(content_choices())[model_pk]


@register.filter
def fix_auth_backend_name(name):
    if name == 'google-oauth2':
        return 'Google'
    if name == 'yandex-openid':
        return 'Yandex'
    if name == 'github':
        return 'GitHub'
    if name == 'vk-oauth2':
        return 'VK'
    return name
