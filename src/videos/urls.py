from django.conf.urls.defaults import *

urlpatterns = patterns('videos.views',
    url(r'^$', 'index', name='index'),
)