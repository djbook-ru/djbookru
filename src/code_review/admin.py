from django.contrib import admin
from .models import Snipet, File, Comment


class FileInline(admin.StackedInline):
    model = File


class SnipetAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'language', 'author', 'created')
    list_filter = ('language',)
    inlines = [FileInline]


class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Snipet, SnipetAdmin)
admin.site.register(Comment, CommentAdmin)
