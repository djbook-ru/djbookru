from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatewords
import datetime
from BeautifulSoup import BeautifulSoup
from dinette.libs.postmarkup import render_bbcode
from accounts.models import User
from django.utils.translation import ugettext_lazy as _

class SiteConfig(models.Model):
    name = models.CharField(_(u'name'), max_length = 100)
    tag_line = models.TextField(_(u'tag line'), max_length = 100)

class SuperCategory(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(blank=True)
    ordering = models.PositiveIntegerField(default = 1)    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User)   
    accessgroups  = models.ManyToManyField(Group,related_name='can_access_forums')
    
    class Meta:
        verbose_name = _("Super Category")
        verbose_name_plural = _("Super Categories")
        ordering = ('-ordering', 'created_on')
        
    def __unicode__(self):
        return self.name
 
    
class Category(models.Model):
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 110)
    description = models.TextField(blank=True)
    ordering = models.PositiveIntegerField(default = 1)
    super_category = models.ForeignKey(SuperCategory)    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, related_name='cposted')
    moderated_by = models.ManyToManyField(User, related_name='moderaters')
    
    class Meta:
        verbose_name = _(u"Category")
        verbose_name_plural = _(u"Categories")
        ordering = ('ordering','-created_on' )    
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            same_slug_count = Category.objects.filter(slug__startswith = slug).count()
            if same_slug_count:
                slug = slug + str(same_slug_count)
            self.slug = slug
        super(Category, self).save(*args, **kwargs)
    
    @models.permalink
    def get_absolute_url(self):
        #return ('welcomePage', [self.slug])
        return ('dinette_index',(),{'categoryslug':self.slug})
    
    def getCategoryString(self):
        return "category/%s" % self.slug
    
    
    def topics(self):
        return self.ftopics_set.filter(is_hidden=False)
    
    def noofPosts(self):
        count = 0
        for topic in self.topics():
            #total posts for this topic = total replies + 1 (1 is for the topic as we are considering it as topic)
            count += topic.reply_set.count() + 1
        ##mlog.debug("TOtal count =%d " % count)
        return count
    
    def lastPostDatetime(self):
        ''' we are assuming post can be topic / reply
         we are finding out the last post / (if exists) last reply datetime '''                
        return self.lastPost().created_on
        
    def lastPostedUser(self):
        '''  we are assuming post can be topic / reply
             we are finding out the last post / (if exists) last reply datetime '''
        return self.lastPost().posted_by.username
     
    def lastPost(self):
        if(self.ftopics_set.count() == 0):
            return self   
        obj = self.ftopics_set.order_by('-created_on')[0]        
        if (obj.reply_set.count() > 0 ):
            return obj.reply_set.order_by("-created_on")[0]
        else :
            return obj  
    
    def __unicode__(self):
        return self.name 
    
class TopicManager(models.Manager):
    def get_query_set(self):
        return super(TopicManager, self).get_query_set().filter(is_hidden = False)
    
    def get_new_since(self, when):
        "Topics with new replies after @when"
        now = datetime.datetime.now()
        return self.filter(last_reply_on__gt = now)

class Ftopics(models.Model):
    category = models.ForeignKey(Category)
    posted_by = models.ForeignKey(User)
    
    subject = models.CharField(_(u'subject'), max_length=999)
    slug = models.SlugField(max_length = 200, db_index = True) 
    message = models.TextField()
    file = models.FileField(upload_to='dinette/files',default='',null=True,blank=True)
    attachment_type = models.CharField(max_length=20,default='nofile')
    filename = models.CharField(max_length=100,default="dummyname.txt")
    viewcount = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)    
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    last_reply_on = models.DateTimeField(auto_now_add=True)
    num_replies = models.PositiveSmallIntegerField(default = 0)
    
    #Moderation features
    announcement_flag = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    is_sticky = models.BooleanField(default=False)
    is_hidden = models.BooleanField(default=False)
    
    default = models.Manager()
    objects = TopicManager()
    
    class Meta:
        ordering = ('-is_sticky', '-last_reply_on',)
        get_latest_by = ('created_on')
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.subject)
            slug = slug[:198]
            same_slug_count = Ftopics.objects.filter(slug__startswith = slug).count()
            if same_slug_count:
                slug = slug + str(same_slug_count)
            self.slug = slug
        super(Ftopics, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return self.subject
    
    @models.permalink
    def get_absolute_url(self):
        return ('dinette_topic_detail',(),{'categoryslug':self.category.slug, 'topic_slug': self.slug})
    
    def htmlfrombbcode(self):
        if(len(self.message.strip()) >  0):            
            return render_bbcode(self.message)
        else :
            return ""
        
    def search_snippet(self):
        msg = "%s %s"% (self.subject, self.message)
        return truncatewords(msg, 50) 
        
    def getTopicString(self):
        #which is helpful for doing reverse lookup of an feed url for a topic         
        return "topic/%s" % self.slug
        
    def lastPostDatetime(self):
        return self.lastPost().created_on
        
    def lastPostedUser(self):
        return self.lastPost().posted_by.username
    
    def lastPost(self):
        if (self.reply_set.count() == 0):
            return self       
        return self.reply_set.order_by('-created_on')[0]        
        
    def classname(self):
        return  self.__class__.__name__

# Create Replies for a topic
class Reply(models.Model):
    topic = models.ForeignKey(Ftopics)
    posted_by = models.ForeignKey(User)
    
    message = models.TextField()
    file = models.FileField(upload_to='dinette/files',default='',null=True,blank=True)
    attachment_type = models.CharField(max_length=20,default='nofile')
    filename = models.CharField(max_length=100,default="dummyname.txt")
    
    reply_number = models.SmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Reply")
        verbose_name_plural = _("Replies")
        ordering = ('created_on',)
        get_latest_by = ('created_on', )
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.reply_number = self.topic.reply_set.all().count() + 1
        super(Reply, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return truncatewords(self.message, 10)
    
    def search_snippet(self):
        msg = "%s %s"%(self.message, self.topic.subject)
        return truncatewords(msg, 100)
    
    @models.permalink
    def get_absolute_url(self):
        return ('dinette_topic_detail',(),{'categoryslug':self.topic.category.slug,'topic_slug': self.topic.slug})
    
    def get_url_with_fragment(self):
        page = (self.reply_number-1)/settings.REPLY_PAGE_SIZE + 1
        url =  self.get_absolute_url()
        if not page == 1:
            return "%s?page=%s#%s" % (url, page, self.reply_number)
        else:
            return "%s#%s" % (url, self.reply_number)
    
    def htmlfrombbcode(self):
        soup = BeautifulSoup(self.message)
        #remove all html tags from the message
        onlytext = ''.join(soup.findAll(text=True))
        
        #get the bbcode for the text
        if(len(onlytext.strip()) >  0):            
            return render_bbcode(onlytext)
        else :
            return ""
    
    def classname(self):
        return  self.__class__.__name__
    
class NavLink(models.Model):
    title = models.CharField(max_length = 100)
    url = models.URLField()
    
    class Meta:
        verbose_name = _("Navigation Link")
        verbose_name_plural = _("Navigation Links")
        
    def __unicode__(self):
        return self.title
        
def update_topic_on_reply(sender, instance, created, **kwargs):
    if created:
        instance.topic.last_reply_on = instance.created_on
        instance.topic.num_replies += 1
        instance.topic.save()
    
post_save.connect(update_topic_on_reply, sender=Reply)

