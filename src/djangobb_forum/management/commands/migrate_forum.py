from django.core.management.base import BaseCommand
from src.accounts.models import User
from src.djangobb_forum.models import Category, Forum
from src.forum import models


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
            new_obj.name = obj.name
            new_obj.position = obj.position
            new_obj.category = models.Category.objects.get(name=obj.category.name)
            new_obj.description = obj.description
            new_obj.save()