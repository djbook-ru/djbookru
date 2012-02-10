from django.conf.urls.defaults import *

urlpatterns = patterns('docbook_translator.views',
    url(r'^$', 'parser', name='parser'),
)