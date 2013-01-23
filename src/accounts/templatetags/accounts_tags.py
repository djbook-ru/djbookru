# -*- coding: utf-8 -*-

from django import template

from ... doc_comments.models import Comment as DocComment
from ... comments.models import Comment
from ..models import Announcement, Achievement

register = template.Library()


@register.inclusion_tag('accounts/_menu.html', takes_context=True)
def profile_menu(context, current):
    return {
        'user': context['user'],
        'current': current
    }


@register.inclusion_tag('accounts/_notification_indicator.html', takes_context=True)
def notification_indicator(context):
    user = context['user']
    new_count = Comment.get_reply_comments(user).count()
    new_count += DocComment.get_reply_comments(user).count()
    return {
        'new_count': new_count
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
