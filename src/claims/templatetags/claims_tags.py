# -*- coding: utf-8 -*-

from django import template
from .. import models

register = template.Library()


@register.inclusion_tag('claims/_claims_statistic.html', takes_context=True)
def claims_statistic(context):
    context['claims'] = models.Claims.statistic()
    return context
