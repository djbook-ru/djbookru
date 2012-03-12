from django.contrib import admin
from models import Chunk


class ChunkAdmin(admin.ModelAdmin):
    list_display = ('key', 'help_column')
    search_fields = ('key', 'content')

    class Media:
        css = {
            'all': ("css/admin.css",)
        }
        js = ['js/admin/force_jquery.js', 'js/jquery.mod.js', 'js/admin/chunks.js']

    def help_column(self, obj):
        if obj.help:
            link = '<a href="#" class="info-link" data-modal="help-content-%s">' % obj.pk
            content = '</a><div class="help-content" id="help-content-%s">%s</div>' % (obj.pk, obj.help)
            return u''.join((link, content))
        return ''
    help_column.short_description = u'Info'
    help_column.allow_tags = True

admin.site.register(Chunk, ChunkAdmin)
