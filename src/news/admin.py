from django.contrib import admin
from news.models import News
from django.conf import settings 

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']

    #class Media:
    #    js = [
    #        settings.ADMIN_MEDIA_PREFIX+'tinymce/jscripts/tiny_mce/tiny_mce.js', 
    #        'js/tinymce_setup.js'
    #    ]
    
admin.site.register(News, NewsAdmin)