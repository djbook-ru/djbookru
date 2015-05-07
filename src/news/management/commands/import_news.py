from datetime import datetime

from django.core.mail import mail_admins
from django.core.management import BaseCommand
from django.db import transaction

import feedparser


def to_datetime(feed_date):
    return datetime(*(feed_date[0:6]))


class Command(BaseCommand):

    def handle(self, *args, **options):
        from src.news.models import ResourceRSS
        updated = False

        for feed in ResourceRSS.objects.filter(is_active=True):
            if self.parse(feed):
                updated = True

        if updated:
            mail_admins(u'Some news imported from RSS!',
                        u'Some news imported from RSS!')

    def parse(self, feed):
        from src.news.models import News

        sync_date = None
        if feed.sync_date:
            sync_date = feed.sync_date.replace(tzinfo=None)
        sync_date = None
        try:
            data = feedparser.parse(feed.link)
        except Exception as e:
            print ('sync failed: %s' % e)
            return

        if 'updated_parsed' not in data.feed.keys():
            updated_date = to_datetime(data.entries[0].published_parsed)
        else:
            updated_date = to_datetime(data.entries[0].updated_parsed)

        if sync_date and sync_date >= updated_date:
            return

        updated = 0
        with transaction.atomic():
            for item in data.entries:
                item_exists = News.objects.filter(link=item.link).exists()
                if item_exists:
                    continue

                news = News(
                    title=item.title,
                    link=item.link,
                    author=feed.news_author,
                    approved=feed.approved_by_default,
                    content=item.summary
                )

                if sync_date and sync_date > to_datetime(item.published_parsed):
                    continue

                news.save()
                updated += 1

            feed.sync_date = updated_date
            feed.save()

        return updated
