# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.translation import ugettext as _

from . import models


class __Claims(admin.ModelAdmin):
    list_display = ('url', 'status_colored', 'status_applied', 'text', 'comment', 'to_page')
    list_filter = ('status',)
    list_per_page = 20

    fieldsets = (
        (_(u'Meta'),
         {'fields': ('url',)}),
        (_(u'Error'),
         {'fields': ('ctx_left', 'selected', 'ctx_right')}),
        (_(u'Comment'),
         {'fields': ('status', 'email', 'comment', 'reply')})
        )

    def status_colored(self, obj):
        output = []
        color = ['yellow', 'orange', 'green', 'red'][obj.status - 1]
        output.append(u'<div style="background-color: %s; padding: 2px 3px; text-align: center">%s</div>' \
               % (color, obj.get_status_display()))
        if obj.notify:
            output.append(u'<div style="background-color: #c0db8a; padding: 2px 3px; text-align: center">%s</div>' \
                % obj.email)
        return u''.join(output)
    status_colored.short_description = _(u'Status')
    status_colored.allow_tags = True

    def to_page(self, obj):
        return u'<a href="%s">GO</a>' % obj.url
    to_page.allow_tags = True

    def text(self, obj):
        output = []
        if obj.ctx_left:
            output.append(u'<span>%s</span>' % obj.ctx_left)
        output.append(u'<span style="background-color: #c0db8a;">%s</span>' % obj.selected)
        if obj.ctx_right:
            output.append(u'<span>%s</span>' % obj.ctx_right)
        return u''.join(output)
    text.allow_tags = True

admin.site.register(models.Claims, __Claims)
