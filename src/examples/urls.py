from django.conf.urls.defaults import *
from examples.feeds import LatestExamplesFeed

urlpatterns = patterns('examples.views',
    url(r'^$', 'index', name='index'),
    url(r'^add/$', 'add', name='add'),
    url(r'^(?P<pk>\d+)/$', 'detail', name='detail'),
    url(r'^c(?P<pk>\d+)/$', 'category', name='category'),
    (r'^feed/$', LatestExamplesFeed()),
)
