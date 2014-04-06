from django.conf.urls import patterns, include, url

from src.forum.models import Topic, Post

urlpatterns = patterns('src.forum.views',
    url(r'^$', 'index', name='index'),
    url(r'^unread_topics/$', 'unread_topics', name='unread_topics'),
    url(r'^my_topics/$', 'my_topics', name='my_topics'),
    url(r'^topic/(\d+)/$', 'topic', name='topic'),
    url(r'^add_post/(\d+)/$', 'add_post', name='add_post'),
    url(r'^add_topic/(\d+)/$', 'add_topic', name='add_topic'),
    url(r'^move_topic/(\d+)/$', 'move_topic', name='move_topic'),
    url(r'^close_open_topic/(\d+)/$', 'close_open_topic', name='close_open_topic'),
    url(r'^stick_unstick_topic/(\d+)/$', 'stick_unstick_topic', name='stick_unstick_topic'),
    url(r'^heresy_unheresy_topic/(\d+)/$', 'heresy_unheresy_topic', name='heresy_unheresy_topic'),
    url(r'^delete_post/(\d+)/$', 'delete_post', name='delete_post'),
    url(r'^delete_topic/(\d+)/$', 'delete_topic', name='delete_topic'),
    url(r'^edit_post/(\d+)/$', 'edit_post', name='edit_post'),
    url(r'^forum/(\d+)/$', 'forum', name='forum'),
    url(r'^mark_read_all/$', 'mark_read_all', name='mark_read_all'),
    url(r'^mark_read_forum/(\d+)/$', 'mark_read_forum', name='mark_read_forum'),
    url(r'^vote/topic/(\d+)/$', 'vote', {'model': Topic}, 'vote_topic'),
    url(r'^vote/post/(\d+)/$', 'vote', {'model': Post}, 'vote_post'),
    url(r'^subscribe/(\d+)/$', 'subscribe', name='subscribe'),
    url(r'^unsubscribe/(\d+)/$', 'unsubscribe', name='unsubscribe'),
)
