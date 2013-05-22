from django.core.management.base import BaseCommand
from src.accounts.models import User
from src.djangobb_forum.models import Category, Forum, Topic, Post
from src.forum import models
from django.utils.html import strip_tags
import htmlentitiesdecode
import re

code_pattern = re.compile(r'<code>(.+?)<\/code>', re.DOTALL)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Migrate Users'
        for user in User.objects.exclude(forum_profile__signature=''):
            user.signature = user.forum_profile.signature
            user.save()

        print 'Migrate Category'
        models.Category.objects.all().delete()

        for obj in Category.objects.all():
            new_obj = models.Category()
            new_obj.name = obj.name
            new_obj.position = obj.position
            new_obj.save()
            new_obj.groups = obj.groups.all()

        print 'migrate Forum'
        models.Forum.objects.all().delete()

        for obj in Forum.objects.all():
            new_obj = models.Forum()
            new_obj.pk = obj.pk
            new_obj.name = obj.name
            new_obj.position = obj.position
            new_obj.category = models.Category.objects.get(name=obj.category.name)
            new_obj.description = obj.description
            new_obj.save()

        print 'migrate Topic'
        models.Topic.objects.all().delete()

        for obj in Topic.objects.all():
            new_obj = models.Topic()
            new_obj.pk = obj.pk
            new_obj.forum_id = obj.forum_id
            new_obj.name = obj.name
            new_obj.updated = obj.updated
            new_obj.user = obj.user
            new_obj.views = obj.views
            new_obj.sticky = obj.sticky
            new_obj.closed = obj.closed
            new_obj.heresy = obj.heresy
            new_obj.save()

            models.Topic.objects.filter(pk=new_obj.pk).update(created=obj.created)

        print 'migrate Post'
        models.Post.objects.all().delete()

        i = 0
        total = Post.objects.count()
        for obj in Post.objects.all():
            i += 1
            if i % 100 == 0:
                print i, 'of', total
            new_obj = models.Post()
            new_obj.pk = obj.pk
            new_obj.topic_id = obj.topic_id
            new_obj.user = obj.user
            new_obj.updated = obj.updated
            new_obj.updated_by = obj.updated_by

            if obj.markup == 'bbcode':
                if '</code>' in obj.body_html:
                    obj.body_html = self.replace_code(obj.body_html)
                new_obj.body = strip_tags(obj.body_html)
            else:
                new_obj.body = obj.body

            new_obj.save()

            models.Post.objects.filter(pk=new_obj.pk).update(created=obj.created)

    def replace_code(self, body):
        def format_code(matchobj):
            code = matchobj.group(1)
            code = code.replace('\n', '\n    ')
            code = '    ' + htmlentitiesdecode.decode(code)
            return '\n'+code+'\n'

        return code_pattern.sub(format_code, body)
