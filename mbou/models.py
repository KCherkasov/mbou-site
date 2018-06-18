# -*- coding: utf-8 -*-
import re
from random import choice

from django.core import validators
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone


class News(models.Model):
    title = models.TextField()
    content = models.TextField()
    pub_date = models.DateTimeField(default = timezone.now)

    def get_by_title(self, title):
        return self.get(title=title)

    def get_by_content(self, content):
        return self.get(content=content)

    def get_by_date(self, date):
        return self.get(pub_date=date)

    def get_url(self):
        return reverse('news', kwargs={'id': self.id, })


class LessonTiming(models.Model):
    number = models.PositiveIntegerField(default=1, validators=[validators.MaxValueValidator(8),
                                                                validators.MinValueValidator(1), ])
    start = models.TimeField()
    end = models.TimeField()


class DocumentCategoryManager(models.Manager):
    def docs_count(self):
        return self.annotate(docs_count=Count('document'))

    def order_by_doc_count(self):
        return self.docs_count().order_by('-docs_count')

    def get_by_name(self, name):
        return self.get(name=name)

    def get_by_name_id(self, name_id):
        return self.get(name_id=name_id)

    def get_or_create(self, name):
        try:
            cat_obj = self.get_by_name(name)
        except DocumentCategory.DoesNotExist:
            cat_obj = self.create(name=name, color=choice(DocumentCategory.COLORS)[0])
            cat_obj.name_id = re.sub(' +', '_', cat_obj.name)
            cat_obj.save()
        return cat_obj

    def get_top_X(self, top_size = 5):
        real_top = top_size
        return self.order_by_doc_count().all()[:real_top]


class DocumentCategory(models.Model):
    GREEN = 'success'
    DBLUE = 'primary'
    BLACK = 'default'
    RED = 'danger'
    LBLUE = 'info'

    COLORS = (('GR', GREEN), ('DB', DBLUE), ('B', BLACK), ('RE', RED), ('BL', LBLUE))

    name = models.CharField(max_length=60)
    name_id = models.CharField(max_length=120, default=u'')
    color = models.CharField(max_length=2, choices=COLORS, default=BLACK)

    objects = DocumentCategoryManager()

    def get_url(self):
        return reverse('docs_by_category', kwargs={'cat_name': self.name_id })

    def __str__(self):
        return '[' + str(self.id) + ']' + self.name


class DocumentQuerySet(models.QuerySet):
    def with_categories(self):
        return self.prefetch_related('categories')

    def with_date_later(self, date):
        return self.filter(pub_date__gt=date)


class DocumentManager(models.Manager):
    def queryset(self):
        query = DocumentQuerySet(self.model, using=self._db)
        return query.with_categories()

    def newest(self):
        return self.order_by('-pub_date')

    def by_category(self, category):
        return self.filter(categories=category)

    def get_by_title(self, title):
        return self.get(title_id=title)


class Document(models.Model):
    title = models.TextField()
    title_id = models.TextField(default=u'')
    description = models.TextField(blank=True)
    doc = models.FileField(upload_to="docs")
    pub_date = models.DateTimeField(default=timezone.now)
    categories = models.ManyToManyField(DocumentCategory)

    objects = DocumentManager()

    def url(self):
        return reverse('document_show', kwargs={'title': self.title_id, })

    def doc_url(self):
        if self.doc and hasattr(self.doc, "url"):
            return self.doc.url
        else:
            return None

    def make_title_id(self):
        return re.sub(' +', '_', self.title)

    class Meta:
        ordering = ['-pub_date']
