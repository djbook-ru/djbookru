from django.contrib.auth.models import UserManager, User as BaseUser
from django.db import models
from django.db.models.signals import post_save
import hashlib
from django.utils.translation import ugettext_lazy as _

class User(BaseUser):
    biography = models.TextField(_(u'biography'), blank=True)
    homepage = models.URLField(_(u'homepage'), verify_exists=False, blank=True)
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _(u'User')
        verbose_name_plural = _(u'Users')
    
    @property
    def comments_count(self):
        if not hasattr(self, '_comments_count'):
            setattr(self, '_comments_count', self.comment_set.count())
        return self._comments_count
    
    @models.permalink
    def get_absolute_url(self):
        return ('accounts:profile', [self.pk])      
    
    def gravatar_photo(self):
        return 'http://www.gravatar.com/avatar/%s.jpg?d=wavatar' % self.getMD5()
    
    def avatar(self):
        return self.gravatar_photo()
    
    def getMD5(self):
        m = hashlib.md5()
        m.update(self.user.email or self.user.username+'@djbook.ru')        
        return m.hexdigest()
    
    @property
    def nickname(self):
        #for easy change of user name display 
        return self.username
        
def create_custom_user(sender, instance, created, **kwargs):
    if created:
        values = {}
        for field in sender._meta.local_fields:
            values[field.attname] = getattr(instance, field.attname)
        user = User(**values)
        user.save()
        
post_save.connect(create_custom_user, BaseUser)