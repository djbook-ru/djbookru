# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from . import forms

urlpatterns = patterns('django.contrib.auth.views',
    url('^login/$', 'login', {'template_name': 'accounts/login.html', 'authentication_form': forms.AuthenticationForm}, 'login'),
    url(r'^password_reset_complete/$', 'password_reset_complete', {
        'template_name': 'accounts/password_reset_complete.html'
    }, 'password_reset_complete'),
)

urlpatterns += patterns('src.accounts.views',
    url(r'^(?P<pk>\d+)/$', 'profile', name='profile'),
    url(r'^create/$', 'create', name='create'),
    url(r'^notifications/$', 'notifications', name='notifications'),
    url(r'^edit/$', 'edit', name='edit'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^resend_confirmation_email/$', 'resend_confirmation_email', name='resend_confirmation_email'),
    url(r'^confirm_email/(?P<confirmation_key>\w+)/$', 'confirm_email', name='confirm_email'),
    url(r'^password_reset/$', 'password_reset', name='password_reset'),
    url(r'^password_reset_confirm/(?P<uidb36>\w+)/(?P<token>[\w\-]+)$', 'password_reset_confirm', name='password_reset_confirm'),
)
