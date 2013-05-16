from .models import UsefulLink
from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin


class UsefulLinkAdmin(OrderedModelAdmin):
    list_display = ('name', 'url', 'move_up_down_links')

admin.site.register(UsefulLink, UsefulLinkAdmin)
