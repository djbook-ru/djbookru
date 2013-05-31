# -*- coding: utf-8 -*-
# (c) 2012 Dmitry Kostochko <alerion.um@gmail.com>
# (c) 2012 Ruslan Popov <ruslan.popov@gmail.com>

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

from adzone.modules import AdClickModule


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for src.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        self.children.append(
            modules.Group(
                _(u'Applications'),
                children=[
                    modules.ModelList(_(u'Content'), [
                        'src.accounts.models.User',
                        'src.examples.models.Example',
                        'src.news.models.News',
                        'src.videos.models.Video',
                    ]),
                    modules.ModelList(_(u'From users'), [
                        'src.doc_comments.models.Comment',
                        'src.claims.models.Claims',
                        'src.comments.models.Comment',
                    ]),
                    modules.ModelList(_(u'Links'), [
                        'src.links.models.*',
                    ]),
                ]
            )
        )

        self.children.append(modules.RecentActions(_('Recent Actions'), 10))
        #self.children.append(AdClickModule(_('AdClick Report')))


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
