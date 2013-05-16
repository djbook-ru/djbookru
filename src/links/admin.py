from .models import UsefulLink, SourceCode, Archive
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin


class UsefulLinkAdmin(OrderedModelAdmin):
    list_display = ('name', 'url', 'move_up_down_links')


class SourceCodeAdmin(OrderedModelAdmin):
    list_display = ('name', 'url', 'move_up_down_links')


class ArchiveAdmin(OrderedModelAdmin):
    list_display = ('name', 'url', 'move_up_down_links')


admin.site.register(UsefulLink, UsefulLinkAdmin)
admin.site.register(SourceCode, SourceCodeAdmin)
admin.site.register(Archive, ArchiveAdmin)
