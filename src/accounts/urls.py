from django.conf.urls.defaults import *
from django.contrib.auth.views import login

urlpatterns = patterns('',
    url('^login/$', login, name='login'),
)

urlpatterns += patterns('accounts.views',
    url(r'^(?P<pk>\d+)/$', 'profile', name='profile'),
    url(r'^create/$', 'create', name='create'),
    url(r'^edit/$', 'edit', name='edit'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^confirm_email/(?P<confirmation_key>\w+)/$', 'confirm_email', name='confirm_email'),
)
