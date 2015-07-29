from django.contrib import admin

from .models import Jobs


class JobsAdmin(admin.ModelAdmin):
    pass

admin.site.register(Jobs, JobsAdmin)
