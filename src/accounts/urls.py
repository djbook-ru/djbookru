# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views

from src.accounts import forms, views

urlpatterns = [
    url(r'^login/$', auth_views.login,
        {
            'template_name': 'accounts/login.html',
            'authentication_form': forms.AuthenticationForm
        },
        name='login'),

    url(r'^password_reset_complete/$', auth_views.password_reset_complete,
        {
            'template_name': 'accounts/password_reset_complete.html'
        },
        name='password_reset_complete'),

    url(r'^password_reset_confirm/(\w+)/([\w\-]+)/$', auth_views.password_reset_confirm,
        {
            'post_reset_redirect': reverse_lazy('accounts:password_reset_complete'),
            'template_name': 'accounts/password_reset_confirm.html'
        },
        name='password_reset_confirm'),

    url(r'^password_reset/$', auth_views.password_reset,
        {
            'template_name': 'accounts/password_reset.html',
            'email_template_name': 'accounts/email_password_reset.html',
            'post_reset_redirect': reverse_lazy('accounts:password_reset_done')
        },
        name='password_reset'),

    url(r'^password_reset_done/$', auth_views.password_reset_done,
        {
            'template_name': 'accounts/password_reset_done.html'
        },
        name='password_reset_done'),

    url(r'^logout/$', auth_views.logout,
        {
            'next_page': '/'
        },
        name='logout')
]

urlpatterns += [
    url(r'^(?P<pk>\d+)/$', views.profile, name='profile'),
    url(r'^voted/topics/(?P<pk>\d+)/$', views.profile_topics, name='profile_more_topics'),
    url(r'^voted/posts/(?P<pk>\d+)/$', views.profile_posts, name='profile_more_posts'),
    url(r'^map/$', views.users_map, name='map'),
    url(r'^save_user_position/$', views.save_user_position, name='save_user_position'),
    url(r'^create/$', views.create, name='create'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^resend_confirmation_email/$', views.resend_confirmation_email,
        name='resend_confirmation_email'),
    url(r'^confirm_email/(?P<confirmation_key>\w+)/$', views.confirm_email, name='confirm_email'),
]
