import re

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from mbou import miscellaneous
from mbou.forms import AddNewsForm, LessonTimingForm, DocumentForm, SignInForm, ProfileEditForm
from mbou.models import News, LessonTiming, Document, DocumentCategory


def index(request):
    return render(request, 'index.html', {"news": News.objects.all, 'year' : timezone.now,
                                          "cats": DocumentCategory.objects.get_top_X, })


def base(request):
    return render(request, 'base.html', {})


def news(request, id):
    try:
        news_entry = News.objects.get(pk=int(id))
    except News.DoesNotExist:
        raise Http404()
    return render(request, "news_one.html", {"n": news_entry, "news": News.objects.all, "year": timezone.now,
                                             "cats": DocumentCategory.objects.get_top_X, })


def news_add(request):
    if request.method == 'POST':
        add = News()
        form = AddNewsForm(request.POST, instance=add)
        if form.is_valid():
            added = form.save()
            return HttpResponseRedirect(reverse('news', kwargs={'id': added.id, }))
    else:
        form = AddNewsForm()
    return render(request, 'news_add.html', {"form": form, "news": News.objects.all, "year": timezone.now,
                                             "cats": DocumentCategory.objects.get_top_X, })


def lesson_edit(request):
    if request.method == "POST":
        form = LessonTimingForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('lessons_show'))
        else:
            form = LessonTimingForm(request.POST)
            return render(request, 'lesson_edit.html', {'form': form, 'news': News.objects.all, "year": timezone.now,
                                                        "cats": DocumentCategory.objects.get_top_X, })
    else:
        form = LessonTimingForm()
    return render(request, 'lesson_edit.html', {'form': form, 'news': News.objects.all, "year": timezone.now,

                                                "cats": DocumentCategory.objects.get_top_X, })


def lessons_show(request):
    lessons = LessonTiming.objects.all().order_by('number')
    return render(request, 'lessons_show.html', {'lessons': lessons, 'news': News.objects.all, "year": timezone.now,
                                                 "cats": DocumentCategory.objects.get_top_X, })


def document_show(request, title):
    try:
        doc = Document.objects.get_by_title(title)
    except Document.DoesNotExist:
        raise Http404()
    doc_namext = re.split('[.]+', doc.doc.name)
    if doc_namext[1] == 'pdf':
        is_pdf = True
    else:
        is_pdf = False
    return render(request, "document.html", {'doc': doc, 'news': News.objects.all, 'year': timezone.now,
                                             'categories': DocumentCategory.objects.order_by_doc_count().all,
                                             "cats": DocumentCategory.objects.get_top_X, 'is_pdf': is_pdf, })


def document_add(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            added = form.save()
            return HttpResponseRedirect(reverse('document_show', kwargs={'title': added.title_id, }))
    else:
        form = DocumentForm()
    return render(request, "document_add.html", {'form': form, 'news': News.objects.all, 'year': timezone.now,
                                                 "cats": DocumentCategory.objects.get_top_X, })


def docs_newest(request):
    documents = Document.objects.newest()
    pagination = miscellaneous.paginate(documents, request, key='document')
    return render(request, 'docs_list.html', {'title': u'Новые документы', 'news': News.objects.all,
                                              'year': timezone.now, 'docs': pagination,
                                              'categories': DocumentCategory.objects.order_by_doc_count().all,
                                              "cats": DocumentCategory.objects.get_top_X, })


def docs_by_category(request, cat_name):
    try:
        cat_obj = DocumentCategory.objects.get_by_name_id(cat_name)
    except DocumentCategory.DoesNotExist:
        raise Http404()
    documents = Document.objects.by_category(cat_obj)
    pagination = miscellaneous.paginate(documents, request, key='document')
    return render(request, 'docs_list.html', {'title': u'Новые документы', 'news': News.objects.all,
                                              'year': timezone.now, 'docs': pagination,
                                              'categories': DocumentCategory.objects.order_by_doc_count().all,
                                              "cats": DocumentCategory.objects.get_top_X, "cat_name": cat_obj.name, })


def gallery_add(request):
    if request.method == 'POST':
        form = GalleryAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('galleries'))
    else:
        form = GalleryAddForm()
    return render(request, 'gallery_add.html', {'form': form, 'news': News.objects.all, "year": timezone.now,
                                                "cats": DocumentCategory.objects.get_top_X, })


def photo_add(request):
    if request.method == 'POST':
        form = PhotoAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('photo_add'))
    else:
        form = PhotoAddForm()
    return render(request, 'photo_add.html', {'form': form, 'year': timezone.now, 'news': News.objects.all,
                                              'cats': DocumentCategory.objects.get_top_X, })


def login(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(redirect)
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            auth.login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(redirect)
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignInForm()
    return render(request, 'login.html', {'form': form, })


@login_required
def edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return HttpResponseRedirect(reverse('index'))
    else:
        user = model_to_dict(request.user)
        form = ProfileEditForm(user)
    return render(request, 'profile_edit.html', {'form': form, 'user': request.user })


@login_required
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)
