from django.contrib.auth.models import UserManager, User as BaseUser
from django.db import models
from django.db.models.signals import post_save
import datetime
import hashlib

class User(BaseUser):
    photo = models.ImageField(upload_to='users/photo',null=True,blank=True)    
    
    #forum profile fields
    last_activity = models.DateTimeField(null=True)
    last_session_activity = models.DateTimeField(null=True)
    userrank = models.CharField(max_length=30,default="Junior Member")
    last_posttime = models.DateTimeField(null=True)
    signature = models.CharField(max_length = 1000, null = True, blank = True)
    
    objects = UserManager()

    @models.permalink
    def get_absolute_url(self):
        return ('accounts:profile', [self.pk])      
    
    #forum profile methods
    def get_total_posts(self):
        print self.user.ftopics_set.count() + self.user.reply_set.count()
        return self.user.ftopics_set.count() + self.user.reply_set.count()
    
    def is_online(self):
        from django.conf import settings
        last_online_duration = getattr(settings, 'LAST_ONLINE_DURATION', 900)
        now = datetime.datetime.now()
        if (now - self.last_activity).seconds < last_online_duration:
            return True
        return False   

    def getMD5(self):
        m = hashlib.md5()
        m.update(self.user.email)        
        return m.hexdigest()
    
    def get_since_last_visit(self):
        "Topics with new relies since last visit"
        from dinette.models import Ftopics
        return Ftopics.objects.get_new_since(self.last_session_activity)
    
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