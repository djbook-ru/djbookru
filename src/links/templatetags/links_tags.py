from django import template
from src.links.models import UsefulLink

register = template.Library()


@register.inclusion_tag('links/_useful_links.html', takes_context=True)
def useful_links(context):
    context['useful_links'] = UsefulLink.objects.all()[:4]
    return context
