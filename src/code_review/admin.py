from django.contrib import admin
from .models import Snipet, File, Comment


class SnipetAdmin(admin.ModelAdmin):
    pass


class FileAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Snipet, SnipetAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Comment, CommentAdmin)