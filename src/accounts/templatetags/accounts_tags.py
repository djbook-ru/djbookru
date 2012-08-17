from django import template
from comments.models import Comment
from doc_comments.models import Comment as DocComment

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
