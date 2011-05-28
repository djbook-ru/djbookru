from django.contrib import admin
from examples.models import Category, Example
from django.conf import settings 
from django.forms import ModelForm
from utils.admin import LogModelAdmin

class CategoryAdmin(admin.ModelAdmin):
    pass

class ExampleForm(ModelForm):
    
    class Meta:
        model = Example
        
    def __init__(self, *args, **kwargs):
        super(ExampleForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs['style'] = 'height: 400px'

class ExampleAdmin(LogModelAdmin):
    list_display = ('title', 'category', 'author', 'approved', 'created')
    list_filter = ('category', 'approved')
    readonly_fields = ('author',)
    form = ExampleForm
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()
        
admin.site.register(Category, CategoryAdmin)
admin.site.register(Example, ExampleAdmin)