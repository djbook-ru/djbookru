from django import template

register = template.Library()


@register.inclusion_tag('accounts/_menu.html', takes_context=True)
def profile_menu(context, current):
    return {
        'user': context['user'],
        'current': current
    }
