from django.contrib import admin
from news.models import News
from django.conf import settings 

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
    
admin.site.register(News, NewsAdmin)