from django.contrib import admin
from news.models import News

class NewsAdmin(admin.ModelAdmin):
    display_fields = ['title']
    
admin.site.register(News, NewsAdmin)