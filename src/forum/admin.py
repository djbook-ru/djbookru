from django.contrib import admin
from .models import Category, Forum


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']
    list_editable = ['position']


class ForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']
    list_editable = ['position']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Forum, ForumAdmin)
