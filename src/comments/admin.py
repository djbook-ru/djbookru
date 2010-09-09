from django.contrib import admin
from django import forms
from comments.models import Comment

class CommentAdminForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['content']

class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = ['content', 'content_type', 'user', 'submit_date']
    search_fields = ('content',)
    
admin.site.register(Comment, CommentAdmin) 