from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from src.forum.feeds import FeedLatestPosts, FeedLatestPostsByForum
from src.forum.models import Topic, Post
from src.forum import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^unread_topics/$', views.unread_topics, name='unread_topics'),
    url(r'^my_topics/$', views.my_topics, name='my_topics'),
    url(r'^topic/(\d+)/$', views.topic, name='topic'),
    url(r'^add_post/(\d+)/$', views.add_post, name='add_post'),
    url(r'^add_topic/(\d+)/$', views.add_topic, name='add_topic'),
    url(r'^move_topic/(\d+)/$', views.move_topic, name='move_topic'),
    url(r'^close_open_topic/(\d+)/$', views.close_open_topic, name='close_open_topic'),
    url(r'^stick_unstick_topic/(\d+)/$', views.stick_unstick_topic, name='stick_unstick_topic'),
    url(r'^heresy_unheresy_topic/(\d+)/$', views.heresy_unheresy_topic, name='heresy_unheresy_topic'),
    url(r'^delete_post/(\d+)/$', views.delete_post, name='delete_post'),
    url(r'^delete_topic/(\d+)/$', views.delete_topic, name='delete_topic'),
    url(r'^edit_post/(\d+)/$', views.edit_post, name='edit_post'),
    url(r'^forum/(\d+)/$', views.forum, name='forum'),
    url(r'^mark_read_all/$', views.mark_read_all, name='mark_read_all'),
    url(r'^mark_read_forum/(\d+)/$', views.mark_read_forum, name='mark_read_forum'),
    url(r'^vote/topic/(\d+)/$', views.vote, {'model': Topic}, 'vote_topic'),
    url(r'^vote/post/(\d+)/$', views.vote, {'model': Post}, 'vote_post'),
    url(r'^subscribe/(\d+)/$', views.subscribe, name='subscribe'),
    url(r'^unsubscribe/(\d+)/$', views.unsubscribe, name='unsubscribe'),
    url(r'^feeds/(?P<forum_id>\d+)/$', FeedLatestPostsByForum(), name='feed_latest_forum_entries'),
    url(r'^feeds/$', FeedLatestPosts(), name='feed_latest_entries'),
    url(r'^statistic/$', views.statistic, name='statistic'),
    url(r'^statistic/posts_per_month_chart\.svg$', views.posts_per_month_chart, name='posts_per_month_chart'),
]
