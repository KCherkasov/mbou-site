import re

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from mbou import categories
from mbou import miscellaneous
from mbou.forms import AddNewsForm, LessonTimingForm, DocumentForm, SignInForm, ProfileEditForm, StaffMemberForm
from mbou.models import News, LessonTiming, Document, DocumentCategory, StaffMember


def index(request):
    return render(request, 'index.html', {"news": News.objects.all, 'year': timezone.now,
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
        documents = Document.objects.by_category(cat_obj)
    except DocumentCategory.DoesNotExist:
        documents = Document.objects.newest()
    pagination = miscellaneous.paginate(documents, request, key='document')
    return render(request, 'docs_list.html', {'title': u'Новые документы', 'news': News.objects.all,
                                              'year': timezone.now, 'docs': pagination,
                                              'categories': DocumentCategory.objects.order_by_doc_count().all,
                                              "cats": DocumentCategory.objects.get_top_X, "cat_name": cat_name, })


def docs_by_cat_name(request, cat_name):
    try:
        cat_obj = DocumentCategory.objects.get_by_name(cat_name)
        documents = Document.objects.by_category(cat_obj)
    except DocumentCategory.DoesNotExist:
        documents = Document.objects.newest()
    pagination = miscellaneous.paginate(documents, request, key='document')
    return render(request, 'docs_list.html', {'title': u'Новые документы', 'news': News.objects.all,
                                              'year': timezone.now, 'docs': pagination,
                                              'categories': DocumentCategory.objects.order_by_doc_count().all,
                                              "cats": DocumentCategory.objects.get_top_X, "cat_name": cat_name, })


def about_main(request):
    return render(request, 'about_main.html', {"news": News.objects.all, 'year': timezone.now,
                                               "cats": DocumentCategory.objects.get_top_X, })


def about_general(request):
    return render(request, 'about_general.html', {"news": News.objects.all, 'year': timezone.now,
                                                  "cats": DocumentCategory.objects.get_top_X, })


def about_education(request):
    return render(request, 'about_education.html', {"news": News.objects.all, 'year': timezone.now,
                                                    "cats": DocumentCategory.objects.get_top_X, })


def about_staff(request):
    return render(request, 'about_staff.html', {"news": News.objects.all, 'year': timezone.now,
                                                "cats": DocumentCategory.objects.get_top_X, })


def about_standards(request):
    return render(request, 'about_standards.html', {"news": News.objects.all, 'year': timezone.now,
                                                    "cats": DocumentCategory.objects.get_top_X, })


def about_structure(request):
    return render(request, 'about_structure.html', {"news": News.objects.all, 'year': timezone.now,
                                                    "cats": DocumentCategory.objects.get_top_X, })


def about_vacancies(request):
    return render(request, 'about_vacancies.html', {"news": News.objects.all, 'year': timezone.now,
                                                    "cats": DocumentCategory.objects.get_top_X, })


def about_docs_all(request):
    return docs_by_cat_name(request, categories.about_docs_category)


def about_financial(request):
    return docs_by_cat_name(request, categories.financial_category)


def about_mto(request):
    return docs_by_cat_name(request, categories.mto_category)


def about_support(request):
    return docs_by_cat_name(request, categories.support_category)


def about_additional(request):
    return docs_by_cat_name(request, categories.additional_category)


def educational_work(request):
    return docs_by_cat_name(request, categories.vosp_category)


def methodical(request):
    return docs_by_cat_name(request, categories.methodical_category)


def curriculum(request):
    return docs_by_cat_name(request, categories.curriculum_category)


def annotations(request):
    return docs_by_cat_name(request, categories.annotations_category)


def main_language(request):
    return docs_by_category(request, categories.main_language_category)


def about_schedules(request):
    return docs_by_cat_name(request, categories.schedules_category)


def programs(request):
    return docs_by_cat_name(request, categories.programs_category)


def credentials(request):
    return docs_by_cat_name(request, categories.credits_category)


def council(request):
    return docs_by_cat_name(request, categories.council_category)


def vacancies(request):
    return docs_by_cat_name(request, categories.vacancies_categories)


def photos(request):
    return docs_by_cat_name(request, categories.photos)


def regional_contests(request):
    return docs_by_cat_name(request, categories.reqional_contests_category)


def school_standard(request):
    return docs_by_cat_name(request, categories.school_standard_category)


def login(request):
    redirect = request.GET.get('continue', '/')
    if request.user.is_authenticated:
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


def staff_list_all(request):
    return render(request, 'staff_teachers.html', {"news": News.objects.all, 'year': timezone.now,
                                                   "cats": DocumentCategory.objects.get_top_X,
                                                   "members": StaffMember.objects.all, })


def staff_list_admin(request):
    members = StaffMember.objects.get_chairmen()
    return render(request, 'staff_admin.html', {"news": News.objects.all, 'year': timezone.now,
                                                "cats": DocumentCategory.objects.get_top_X,
                                                "members": members, })


def staff_list_elementary(request):
    members = StaffMember.objects.get_elementary_teachers()
    return render(request, 'staff_elementary.html', {"news": News.objects.all, 'year': timezone.now,
                                                     "cats": DocumentCategory.objects.get_top_X,
                                                     "members": members, })


def staff_list_not_elementary(request):
    members = StaffMember.objects.get_not_elementary_teachers()
    return render(request, 'staff_not_elementary.html', {"news": News.objects.all, 'year': timezone.now,
                                                         "cats": DocumentCategory.objects.get_top_X,
                                                         "members": members, })


def staff_member_add(request):
    if request.method == 'POST':
        form = StaffMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff_all'))
    else:
        form = StaffMemberForm()
    return render(request, 'staff_member_form_add.html', {"news": News.objects.all, 'year': timezone.now,
                                                          "cats": DocumentCategory.objects.get_top_X,
                                                          "form": form, })


def staff_member_edit(request, full_name):
    if request.method == 'POST':
        form = StaffMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('staff_all'))
    else:
        try:
            staffer = StaffMember.objects.get_by_full_name(full_name=full_name)
        except StaffMember.DoesNotExist:
            raise Http404()
        model = model_to_dict(staffer)
        form = StaffMemberForm(model)
    return render(request, 'staff_member_form_edit.html', {"news": News.objects.all, 'year': timezone.now,
                                                           "cats": DocumentCategory.objects.get_top_X,
                                                           "form": form, })


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
    return render(request, 'profile_edit.html', {'form': form, 'user': request.user, })


@login_required
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)
