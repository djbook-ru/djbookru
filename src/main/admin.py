# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms
from main.models import Book, Page
from django.utils.translation import gettext_lazy as _
from StringIO import StringIO
from zipfile import ZipFile, BadZipfile
import re

class BookAdminForm(forms.ModelForm):
    archive = forms.FileField(required=False)
    
    class Meta:
        model = Book
        fields = ('name', 'description', 'archive', 'toc')
    
    def clean_archive(self):
        archive = self.cleaned_data['archive']
        
        if archive:
            try:
                error = ZipFile(archive).testzip()
            except BadZipfile:
                error = True
            finally:
                if error:
                    raise forms.ValidationError(_(u'This should be zip archive'))
        
        return archive
    
    def update_from_archive(self, archive, obj):
        Page.objects.filter(book=obj).delete()
        archive = ZipFile(archive)
        
        toc = archive.read('toc.py')
        toc = toc.replace('(', '[').replace(')', ']').replace("'", '"')
        obj.toc = toc
        obj.save()
        
        appendix_pattern = re.compile(r'^ap(?P<section>[a-z])\.html$')
        ch_pattern = re.compile(r'^ch(?P<ch>\d+)\.html$')
        chs_pattern = re.compile(r'^ch(?P<ch>\d+)s(?P<s>\d+)\.html$')
        
        for filename in archive.namelist():
            if not filename.split('.')[-1] == 'html':
                continue
            
            if filename == 'index.html':
                name = u'Первая страница'
            elif chs_pattern.match(filename):
                r = chs_pattern.match(filename)
                #FIXME: fix numbers 01 == 1
                name = u'Глава %s, раздел %s' % (r.group('ch'), r.group('s'))
            elif ch_pattern.match(filename):
                r = ch_pattern.match(filename)
                name = u'Глава %s' % r.group('ch')
            elif appendix_pattern.match(filename):
                r = appendix_pattern.match(filename)
                name = u'Приложение %s' % r.group('section').upper()
            else:
                name = filename
            
            page = Page(name=name, slug=filename[:-5])
            page.content=archive.read(filename)
            page.book = obj
            page.save()
            
        archive.close()
                
    def save(self, commit=True):
        obj = super(BookAdminForm, self).save(commit)
        archive = self.cleaned_data['archive']
        
        if archive:
            self.update_from_archive(archive, obj)
        
        return obj
        
    
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'created']
    form = BookAdminForm
    
admin.site.register(Book, BookAdmin)