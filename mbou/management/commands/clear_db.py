from django.core.management.base import BaseCommand

from mbou.models import News, LessonTiming, Document, DocumentCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        # lessons = Schedule.objects.all()
        # lessons.delete()
        news = News.objects.all()
        news.delete()
        docs = Document.objects.all()
        docs.delete()
        cats = DocumentCategory.objects.all()
        cats.delete()
