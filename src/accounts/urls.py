# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

from . import forms

urlpatterns = patterns(
    'django.contrib.auth.views',

    url('^login/$', 'login',
        {
            'template_name': 'accounts/login.html',
            'authentication_form': forms.AuthenticationForm
        },
        name='login'),

    url(r'^password_reset_complete/$', 'password_reset_complete',
        {
            'template_name': 'accounts/password_reset_complete.html'
        },
        name='password_reset_complete'),

    url(r'^password_reset_confirm/(\w+)/([\w\-]+)/$', 'password_reset_confirm',
        {
            'post_reset_redirect': reverse_lazy('accounts:password_reset_complete'),
            'template_name': 'accounts/password_reset_confirm.html'
        },
        name='password_reset_confirm'),

    url(r'^password_reset/$', 'password_reset',
        {
            'template_name': 'accounts/password_reset.html',
            'email_template_name': 'accounts/email_password_reset.html',
            'post_reset_redirect': reverse_lazy('accounts:password_reset_done')
        },
        name='password_reset'),
    url(r'^password_reset_done/$', 'password_reset_done',
        {
            'template_name': 'accounts/password_reset_done.html'
        },
        name='password_reset_done')
)

urlpatterns += patterns(
    'src.accounts.views',
    url(r'^(?P<pk>\d+)/$', 'profile', name='profile'),
    url(r'^voted/topics/(?P<pk>\d+)/$', 'profile_topics', name='profile_more_topics'),
    url(r'^voted/posts/(?P<pk>\d+)/$', 'profile_posts', name='profile_more_posts'),
    url(r'^map/$', 'user_map', name='map'),
    url(r'^save_user_position/$', 'save_user_position', name='save_user_position'),
    url(r'^create/$', 'create', name='create'),
    url(r'^notifications/$', 'notifications', name='notifications'),
    url(r'^edit/$', 'edit', name='edit'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^resend_confirmation_email/$', 'resend_confirmation_email',
        name='resend_confirmation_email'),
    url(r'^confirm_email/(?P<confirmation_key>\w+)/$', 'confirm_email', name='confirm_email'),
)
