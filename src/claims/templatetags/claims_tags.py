from django import template
from claims.models import Claims

register = template.Library()

@register.inclusion_tag('claims/_claims_statistic.html', takes_context=True)
def claims_statistic(context):
    context['claims'] = Claims.statistic()
    return context