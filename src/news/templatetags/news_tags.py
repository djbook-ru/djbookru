from django import template
from news.models import News
from django.conf import settings

register = template.Library()

NEWS_ON_PAGE = getattr(settings, 'NEWS_ON_PAGE', 3)


@register.inclusion_tag('news/_last_news.html')
def last_news():
    return {
        'news': News.objects.all()[:NEWS_ON_PAGE]
    }
