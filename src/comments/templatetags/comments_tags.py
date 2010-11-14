from django import template
from comments.forms import CommentForm
from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

register = template.Library()

LAST_COMMENTS_COUNT = getattr(settings, 'LAST_COMMENTS_COUNT', 10)

@register.inclusion_tag('comments/form.html', takes_context=True)
def render_comment_form(context, obj):
    if context['user'].is_authenticated():
        form = CommentForm(obj, auto_id='id_comment_form_%s')
    else:
        form = None
    return {
        'form': form,
        'next_page': context['request'].get_full_path(),
        'perms': context['perms'],
        'user': context['user']
    }

@register.inclusion_tag('comments/list.html', takes_context=True)
def render_comment_list(context, obj):
    return {
        'qs': Comment.get_for_object(obj),
        'content_type': ContentType.objects.get_for_model(obj),
        'obj': obj,
        'perms': context['perms'],
        'user': context['user']
    }
    
@register.simple_tag    
def get_comment_count(obj):
    return Comment.get_for_object(obj).count()

@register.inclusion_tag('comments/last_comments.html', takes_context=True)
def last_comments(context):
    context['last_comments'] = Comment.objects.order_by('-submit_date')[:LAST_COMMENTS_COUNT]
    return context