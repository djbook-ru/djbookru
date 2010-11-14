from django.contrib import admin
from examples.models import Category, Example
from django.conf import settings 

class CategoryAdmin(admin.ModelAdmin):
    pass

class ExampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created')
    list_filter = ('category',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
        
admin.site.register(Category, CategoryAdmin)
admin.site.register(Example, ExampleAdmin)