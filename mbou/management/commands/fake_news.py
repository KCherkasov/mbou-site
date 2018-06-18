from django.core.management.base import BaseCommand

from mbou.models import News


class Command(BaseCommand):
    help = "creates fake news"

    def handle(self, *args, **options):
        number = 12
        for i in range(0, number):
            n = News()
            n.title = "Test news title number " + str(i)
            n.content = "Test news content number " + str(i)
            n.save()
            self.stdout.write("[%d] added news entry %s" % (i, n.title))
