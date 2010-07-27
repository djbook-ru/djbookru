from django.conf.urls.defaults import *
from django.contrib.auth.views import login

urlpatterns = patterns('',
    url('^login/$', login, name='login'),
    url('^logout/$', 'accounts.views.logout', name='logout'),
)