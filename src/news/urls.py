from django.conf.urls.defaults import *
from news.feeds import LatestNewsFeed

urlpatterns = patterns('news.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<pk>\d+)/$', 'news', name='news'),
    (r'^feed/$', LatestNewsFeed()),
)
