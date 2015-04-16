# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import template

from src.accounts.models import Announcement, Achievement
from src.comments.models import Comment
from src.doc_comments.models import Comment as DocComment

register = template.Library()


@register.inclusion_tag('accounts/_menu.html', takes_context=True)
def profile_menu(context, current=None):
    return {
        'user': context['user'],
        'current': current
    }


@register.inclusion_tag('accounts/_announcements.html', takes_context=True)
def announcements(context):
    return {
        'announcements': Announcement.objects.filter(is_active=True)
    }


@register.inclusion_tag('accounts/_achievements.html', takes_context=True)
def achievements(context, user, theme=None):
    return {
        'theme': theme,
        'user_achivements': Achievement.objects.filter(userachievement__user=user),
        'user_obj': user,
        'achivements': Achievement.objects.all()
    }
