from django.core.management.base import BaseCommand

from mbou.models import Document, DocumentCategory
import mbou.categories as categories

class Command(BaseCommand):
    help = "adds tags to doc"

    def handle(self, *args, **options):
        tag1 = DocumentCategory.objects.get_by_name(categories.about_docs_category)
        tag2 = DocumentCategory.objects.get_by_name(categories.mto_category)
        tag3 = DocumentCategory.objects.get_by_name(categories.mealorg)
        documents = Document.objects.by_category(tag3)
        for doc in documents:
            if tag1 not in doc.categories.all():
                doc.categories.add(tag1)
            if tag2 not in doc.categories.all():
                doc.categories.add(tag2)
            doc.save()
