# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _
from claims import models

class __Claims(admin.ModelAdmin):
    list_display = ('url', 'status_colored', 'status_applied', 'comment', 'email', 'notify')
    list_filter = ('status',)

    fieldsets = (
        (_(u'Meta'),
         {'fields': ('url',)}),
        (_(u'Error'),
         {'fields': ('ctx_left', 'selected', 'ctx_right')}),
        (_(u'Comment'),
         {'fields': ('status', 'email','comment', 'reply')})
        )

    def status_colored(self, claim):
        color = ['yellow', 'orange', 'green', 'red'][claim.status - 1]
        return '<div style="background-color: %s; padding: 2px 3px; text-align: center">%s</div>' \
               % (color, claim.get_status_display())
    status_colored.short_description = _(u'Status')
    status_colored.allow_tags = True

admin.site.register(models.Claims, __Claims)
