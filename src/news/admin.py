from django.contrib import admin
from news.models import News
from django.conf import settings 

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']
    
admin.site.register(News, NewsAdmin)