from django.conf.urls import patterns, include, url


urlpatterns = patterns('src.forum.views',
    url(r'^$', 'index', name='index'),
    url(r'^topic/(\d+)/$', 'topic', name='topic'),
    url(r'^add_post/(\d+)/$', 'add_post', name='add_post'),
    url(r'^add_topic/(\d+)/$', 'add_topic', name='add_topic'),
    url(r'^delete_post/(\d+)/$', 'delete_post', name='delete_post'),
    url(r'^delete_topic/(\d+)/$', 'delete_topic', name='delete_topic'),
    url(r'^edit_post/(\d+)/$', 'edit_post', name='edit_post'),
    url(r'^forum/(\d+)/$', 'forum', name='forum'),
    url(r'^mark_read_all/$', 'mark_read_all', name='mark_read_all'),
    url(r'^mark_read_forum/(\d+)/$', 'mark_read_forum', name='mark_read_forum'),

)
