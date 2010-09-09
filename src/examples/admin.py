from django.contrib import admin
from examples.models import Category, Example
from django.conf import settings 

class CategoryAdmin(admin.ModelAdmin):
    pass

class ExampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created')
    list_filter = ('category',)
    
    class Media:
        js = [
            settings.ADMIN_MEDIA_PREFIX+'tinymce/jscripts/tiny_mce/tiny_mce.js', 
            'js/tinymce_setup.js'
        ]
        
admin.site.register(Category, CategoryAdmin)
admin.site.register(Example, ExampleAdmin)