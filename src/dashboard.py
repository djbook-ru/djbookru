# -*- coding: utf-8 -*-
# (c) 2012 Dmitry Kostochko <alerion.um@gmail.com>
# (c) 2012 Ruslan Popov <ruslan.popov@gmail.com>

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

from adzone.modules import AdClickReport


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for src.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(
            modules.LinkList(
                _(u'Quick Links'),
                layout='inline',
                draggable=False,
                deletable=False,
                collapsable=False,
                children=[
                    (_(u'Go to Site'), reverse('main:index')),
                    [_(u'Error Console'), reverse('sentry')],
                    [_('Change password'), reverse('%s:password_change' % site_name)],
                    [_('Log out'), reverse('%s:logout' % site_name)],
                ]))

        self.children.append(
            modules.Group(
                _(u'Administration'),
                children=[
                modules.ModelList(_(u'Credentials'), [
                    'accounts.models.User',
                    'django.contrib.auth.models.Group',
                    ]),
                modules.AppList(_(u'Control'), models=(
                    'google_analytics.*', 'django.contrib.*',

                    ))
                ]))

        self.children.append(
            modules.Group(
                _(u'Applications'),
                children=[
                modules.ModelList(_(u'Content'), [
                    'src.news.models.News',
                    'src.claims.models.Claims',
                    'src.comments.models.Comment',
                    'src.videos.models.Video',
                    'src.accounts.Announcement'
                    ]),
                modules.ModelList(_(u'Book'), [
                    'src.main.models.Book',
                    'src.main.models.Page',
                    ]),
                modules.ModelList(_(u'Receipts'), [
                    'src.examples.models.Example',
                    'src.examples.models.Category',
                    ]),
                modules.ModelList(_(u'Documentation'), [
                    'src.doc_comments.models.Comment',
                    ]),
                modules.ModelList(_(u'Advertisment'), [
                    'adzone.models.Advertiser',
                    'adzone.models.AdCategory',
                    'adzone.models.AdZone',
                    'adzone.models.TextAd',
                    'adzone.models.BannerAd',
                    'adzone.models.AdClick',
                    'adzone.models.Impression',
                    ]),
                modules.ModelList(_(u'Forum'), [
                    'src.djangobb_forum.models.Category',
                    'src.djangobb_forum.models.Forum',
                    'src.djangobb_forum.models.Topic',
                    'src.djangobb_forum.models.Post',
                    'src.djangobb_forum.models.PostTracking',
                    ])
                ]))

        self.children.append(modules.RecentActions(_('Recent Actions'), 10))
        self.children.append(AdClickReport(_('AdClick Report')))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for src.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
