from .forms import VideoAdminForm
from .models import Video
from django.contrib import admin


class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    list_display = ['title', 'tags']

admin.site.register(Video, VideoAdmin)
