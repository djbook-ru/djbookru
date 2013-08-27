from django.contrib import admin
from .models import Category, Forum, Topic


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']
    list_editable = ['position']


class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'position']
    list_editable = ['position']
    search_fields = ('name',)


class TopicAdmin(admin.ModelAdmin):
    list_filter = ['sticky', 'closed', 'heresy']
    list_display = ['name', 'forum', 'created', 'updated', 'user', 'views', 'sticky']
    search_fields = ('name',)

admin.site.register(Topic, TopicAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
