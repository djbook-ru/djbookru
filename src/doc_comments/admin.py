from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['created', 'comment', 'url', 'author']

    def url(self, obj):
        return '<a href="%s">%s</a>' % (obj.page, obj.page_title)
    url.allow_tags = True

    def comment(self, obj):
        return obj.get_content()
    comment.allow_tags = True

admin.site.register(Comment, CommentAdmin)