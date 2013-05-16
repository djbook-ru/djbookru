from django import template
from src.links.models import UsefulLink, SourceCode, Archive

register = template.Library()


@register.inclusion_tag('links/_useful_links.html', takes_context=True)
def useful_links(context):
    context['useful_links'] = UsefulLink.objects.all()[:4]
    return context


@register.inclusion_tag('links/_source_codes.html', takes_context=True)
def source_codes(context):
    context['source_codes'] = SourceCode.objects.all()[:5]
    return context


@register.inclusion_tag('links/_archive.html', takes_context=True)
def archive(context):
    context['archive_links'] = Archive.objects.all()[:5]
    return context
