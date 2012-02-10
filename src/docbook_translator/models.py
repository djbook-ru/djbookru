from django.db import models
from django.utils.translation import ugettext_lazy as _
from accounts.models import User
from datetime import datetime

class Language(models.Model):
    code = models.CharField(max_length=3, help_text=_(u'Language code in ISO 693-1 or other'))
    name = models.CharField(max_length=100)
    original_name = models.CharField(max_length=100, blank=True)
    
    def __unicode__(self):
        if self.original_name:
            return u'%s(%s)' % (self.name, self.original_name)
        return self.name
    
class Book(models.Model):
    original_name = models.CharField(max_length=1000)
    original_description = models.TextField()
    original_language = models.ForeignKey(Language)
    
    name = models.CharField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    language = models.ForeignKey(Language, related_name='translated_books')
    
    moderators = models.ManyToManyField(User, blank=True, related_name='moderated_books')
    translators = models.ManyToManyField(User, blank=True, related_name='translated_books')
    locked = models.BooleanField(default=False, help_text=_(u'This book can be translated only by moderators and translators'))
    completed = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.original_name
    
class Chapter(models.Model):
    DOCBOOK = 1
    book = models.ForeignKey(Book)
    
    original_name = models.CharField(max_length=1000)
    original_description = models.TextField(blank=True)
    original_text = models.TextField()
    
    namber = models.IntegerField(default=1)
    type = models.IntegerField(default=DOCBOOK, editable=False)
    
    name = models.CharField(max_length=1000, blank=True)
    description = models.TextField(blank=True)
    text = models.TextField()
    
    locked = models.BooleanField(default=False, help_text=_(u'This chapter can be translated only by moderators and translators'))
    completed = models.BooleanField(default=False, help_text=_(u'This chapter is completed and can be changed only by moderators'))
    visible = models.BooleanField(default=True, help_text=_(u'This chapter is visible on site'))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.original_name
    
class TextNode(models.Model):
    TITLE = 1
    PARA = 2
    START_PARA = 3
    END_PARA = 4
    TYPE_CHOICES = (
        (TITLE, _(u'<title>')),
        (PARA, _(u'<para>')),
        (END_PARA, _(u'End <para>')),
        (START_PARA, _(u'Start <para>'))
    )
    chapter = models.ForeignKey(Chapter)
    original_text = models.TextField()
    text = models.TextField(blank=True)
    number = models.IntegerField(help_text=_(u'Order number in XML tree'))
    type = models.IntegerField(choices=TYPE_CHOICES, default=PARA)
    path = models.CharField(max_length=500, help_text=_(u'Path in XML tree'))
    
    locked = models.BooleanField(default=False, help_text=_(u'This chapter can be translated only by moderators and translators'))
    completed = models.BooleanField(default=False, help_text=_(u'This chapter can be changed only by moderators and text is filed with tanslation'))

class TextNodeVersion(models.Model):
    text_node = models.ForeignKey(TextNode)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    moderator_rating = models.IntegerField(default=0)
    approved = models.BooleanField(default=False, help_text=_(u'This version is marked as the best translation'))
    number = models.IntegerField(editable=False)
    
    author = models.ForeignKey(User, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = (('text_node', 'approved'),)
        
class Comment(models.Model):
    text_node = models.ForeignKey(TextNode)
    comment = models.TextField()
    author = models.ForeignKey(User, related_name="translator_comments")
    created = models.DateTimeField(auto_now_add=True)