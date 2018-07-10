# -*- coding: utf-8 -*-
import re
from random import choice

from django.core import validators
from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils import timezone

from mbou import subjects


class News(models.Model):
    title = models.TextField()
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    views_count = models.PositiveIntegerField(default=0)

    def get_by_title(self, title):
        return self.get(title=title)

    def get_by_content(self, content):
        return self.get(content=content)

    def get_by_date(self, date):
        return self.get(pub_date=date)

    def get_url(self):
        return reverse('news', kwargs={'id': self.id, })

    class Meta:
        ordering = ['-pub_date', '-views_count']


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

    def get_top_X(self, top_size=5):
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
        return reverse('docs_by_category', kwargs={'cat_name': self.name_id})

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
    views_count = models.IntegerField(default=0)

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
        ordering = ['-pub_date', '-views_count']


class SubjectManager(models.Manager):
    def get_by_title(self, title):
        return self.get(title=title)

    def get_or_create(self, title):
        try:
            sub_obj = self.get_by_title(title)
        except Subject.DoesNotExist:
            sub_obj = self.create(title=title)
            sub_obj.save()
        return sub_obj


class Subject(models.Model):
    title = models.TextField()

    objects = SubjectManager()

    def __str__(self):
        return self.title


class StafferCategoryManager(models.Manager):
    def get_by_title(self, title):
        return self.get(title=title)

    def get_or_create(self, title):
        try:
            cat_obj = self.get_by_title(title)
        except StafferCategory.DoesNotExist:
            cat_obj = self.create(title=title)
            cat_obj.save()
        return cat_obj


class StafferCategory(models.Model):
    title = models.TextField()

    objects = StafferCategoryManager()

    def __str__(self):
        return self.title


class StaffMemberQuerySet(models.QuerySet):
    def with_category(self):
        return self.prefetch_related('category')

    def with_subject(self):
        return self.prefetch_related('subject')


class StaffMemberManager(models.Manager):
    def queryset(self):
        query = StaffMemberQuerySet(self.model, using=self._db)
        return query.with_category().with_subject()

    def get_chairmen(self):
        return self.queryset().filter(is_chairman=True)

    def get_elementary_teachers(self):
        return self.queryset().filter(subject__title=subjects.elementary)

    def get_not_elementary_teachers(self):
        return self.queryset().all().exclude(subject__title=subjects.elementary)

    def get_by_full_name(self, full_name):
        return self.queryset().get(full_name=full_name)


class StaffMember(models.Model):
    first_name = models.TextField()
    middle_name = models.TextField()
    last_name = models.TextField()
    full_name = models.TextField(default=u'')
    is_chairman = models.BooleanField(default=False)
    chair_position = models.TextField(default='')
    is_combiner = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, default=None, on_delete=models.SET_DEFAULT)
    category = models.ForeignKey(StafferCategory, default=None, on_delete=models.SET_DEFAULT)
    email = models.EmailField(default='')
    experience = models.IntegerField(default=0)

    objects = StaffMemberManager()

    def get_full_name(self):
        return self.first_name + '_' + self.middle_name + '_' + self.last_name

    def get_edit_url(self):
        return reverse('edit_staff_member', kwargs={'full_name': self.full_name})

    @staticmethod
    def add_or_update(first_name, middle_name, last_name, is_chairman, chair_position,
                      is_combiner, subject, category, email, experience):
        new_full_name = first_name + '_' + middle_name + '_' + last_name
        new_subject = Subject.objects.get_or_create(subject)
        new_category = StafferCategory.objects.get_or_create(category)
        old, new = StaffMember.objects.update_or_create(full_name=new_full_name,
                                                        defaults={'first_name': first_name, 'middle_name': middle_name,
                                                                  'last_name': last_name, 'full_name': new_full_name,
                                                                  'is_chairman': is_chairman,
                                                                  'chair_position': chair_position,
                                                                  'is_combiner': is_combiner, 'subject': new_subject,
                                                                  'category': new_category, 'email': email,
                                                                  'experience': experience})
        return new


class AlbumQueryset(models.QuerySet):
    def with_photos(self):
        query = self.prefetch_related('photo_set')
        return query

    def with_photos_count(self):
        return self.annotate(photos_count=Count('photos__id', distinct=True))


class AlbumManager(models.Manager):
    def queryset(self):
        queryset = AlbumQueryset(self.model, using=self._db)
        return queryset.with_photos_count()

    def single(self, title_id):
        return self.queryset().with_photos().get(pk=title_id)


class Album(models.Model):
    title = models.TextField(max_length=60, default=u'')
    title_id = models.TextField(max_length=70, default=u'', primary_key=True)
    description = models.TextField(max_length=360, default=u'')
    pub_date = models.DateTimeField(default=timezone.now)
    photos_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)

    objects = AlbumManager()

    def __str__(self):
        return self.title

    def make_title_id(self):
        return re.sub(' +', '_', self.title)

    def get_url(self):
        return reverse('albums', kwargs={'album_id': self.title_id, })

    def photo_add_url(self):
        return reverse('add_photo_certain', kwargs={'album_id': self.title_id, })

    class Meta:
        ordering = ['-pub_date', '-views_count']


class Photo(models.Model):
    label = models.TextField(max_length=60, default=u'')
    description = models.TextField(max_length=360, default=u'')
    photo = models.ImageField(upload_to='photos')
    pub_date = models.DateTimeField(default=timezone.now)
    album = models.ForeignKey(Album, default=None, on_delete=models.SET_DEFAULT)

    def __str__(self):
        return self.label

    def get_by_id(self, id):
        return self.get(id=id)

    def photo_url(self):
        if self.photo and hasattr(self.photo, "url"):
            return self.photo.url
        else:
            return None

    class Meta:
        ordering = ['-pub_date']
