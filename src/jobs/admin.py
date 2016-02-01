from django.contrib import admin

from .models import Jobs


class JobsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'company_name_slug': ('company_name',)}

admin.site.register(Jobs, JobsAdmin)
