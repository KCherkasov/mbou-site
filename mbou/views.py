from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from mbou import settings
from mbou import categories
from mbou import miscellaneous
from mbou.forms import AddNewsForm, LessonTimingForm, DocumentForm, SignInForm, \
    ProfileEditForm, StaffMemberForm, PhotoAddForm, AlbumAddForm, UrlUserCreationForm, DocumentSearchForm, FoodTableForm
from mbou.models import News, LessonTiming, Document, DocumentCategory, StaffMember, Album, UrlUser, FoodTable


def index(request):
    return render(request, 'index.html', {"news": News.objects.all, 'year': timezone.now,
                                          "cats": DocumentCategory.objects.get_top_X,
                                          "top_news": News.objects.get_top_X, })


def base(request):
    return render(request, 'base.html', {})


def news(request, id):
    try:
        news_entry = News.objects.get(pk=int(id))
        news_entry.views_count = news_entry.views_count + 1
        news_entry.save()
    except News.DoesNotExist:
        raise Http404()
    return render(request, "news_one.html", {"n": news_entry, "news": News.objects.all, "year": timezone.now,
                                             "cats": DocumentCategory.objects.get_top_X, })

def external_links(request):
    return render(request, 'useful_links.html', {"news": News.objects.all, 'year': timezone.now,
                                                 "cats": DocumentCategory.objects.get_top_X, })

@login_required
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


@login_required
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
        doc.views_count = doc.views_count + 1
        doc.save()
    except Document.DoesNotExist:
        raise Http404()
    doc_namext = doc.doc.name.split('.', maxsplit=2)
    if doc_namext[1] == 'pdf':
        is_pdf = True
    else:
        is_pdf = False
    return render(request, "document.html", {'doc': doc, 'news': News.objects.all, 'year': timezone.now,
                                             'categories': DocumentCategory.objects.order_by_doc_count().all,
                                             "cats": DocumentCategory.objects.get_top_X, 'is_pdf': is_pdf, })


@login_required
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

def food_table_show(request, name):
    try:
        ft = FoodTable.objects.get_by_title(name)
        doc_namext = ft.doc.name.split('.', maxsplit=2)
        ft.views_count = ft.views_count + 1
        ft.save()
    except FoodTable.DoesNotExist:
        raise Http404()
    if doc_namext[1] == 'pdf':
        is_pdf = True
    else:
        is_pdf = False
    return render(request, "food_table_show.html", {'ft': ft, 'news': News.objects.all, 'year': timezone.now,
                                             "cats": DocumentCategory.objects.get_top_X, 'is_pdf': is_pdf, })

def food_table_list(request):
    fts = FoodTable.objects.all()
    pagination = miscellaneous.paginate(fts, request, key='fts')
    return render(request, 'food_table_list.html', {'title': u'Питание учащихся (таблицы меню)', 'news': News.objects.all,
                                                    'year': timezone.now, 'fts': pagination,
                                                    "cats": DocumentCategory.objects.get_top_X, })

@login_required
def food_table_add(request):
    if request.method == 'POST':
        form = FoodTableForm(request.POST, request.FILES)
        if form.is_valid():
            added = form.save()
            return HttpResponseRedirect(reverse('food_table_show', kwargs={'name' : added.title_id, }))
    else:
        form = FoodTableForm()
    return render(request, 'food_table_add.html', {'form': form, 'news': News.objects.all, 'year': timezone.now,
                                                 "cats": DocumentCategory.objects.get_top_X, })

def food_table_get(request, name):
    print(name)
    sh_name = str(name.split('.',maxsplit=2)[0])
    print(sh_name)
    try:
        ft = FoodTable.objects.get_by_title(sh_name)
        with open(settings.MEDIA_ROOT[:-6]+str(ft.doc_url()), 'rb') as file:
            file_data = file.read()
        response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="' + name + '"'
    except FoodTable.DoesNotExist:
        raise Http404()
    except IOError:
        response = render(request, 'food_table_list.html', {'title': u'Питание учащихся (таблицы меню)', 'news': News.objects.all,
                                                    'year': timezone.now, 'fts': pagination,
                                                    "cats": DocumentCategory.objects.get_top_X, })
    return response;

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
    return render(request, 'docs_list.html', {'title': u'Документы по категории', 'news': News.objects.all,
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
    return render(request, 'docs_list.html', {'title': u'Документы по категории', 'news': News.objects.all,
                                              'year': timezone.now, 'docs': pagination,
                                              'categories': DocumentCategory.objects.order_by_doc_count().all,
                                              "cats": DocumentCategory.objects.get_top_X, "cat_name": cat_name, })

def docs_search_result(request, query):
    result = Document.objects.search_by_title(query)
    pagination = miscellaneous.paginate(result, request, key='document')
    return render(request, 'docs_list.html', {'title': u'Результаты поиска', 'news': News.objects.all,
                                              'year': timezone.now, 'docs': pagination,
                                              'categories': DocumentCategory.objects.order_by_doc_count().all,
                                              "cats": DocumentCategory.objects.get_top_X, "query": query})

def docs_search(request):
    if request.method == 'POST':
        form = DocumentSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            return HttpResponseRedirect(reverse('docs_search_result', kwargs={ 'query': query }))
        else:
            return HttpResponseRedirect(reverse('docs_search'))
    else:
        form = DocumentSearchForm()
    return render(request, 'docs_search.html', {'title': u'Поиск документов', 'news': News.objects.all,
                                                'year': timezone.now, "cats": DocumentCategory.objects.get_top_X,
                                                'form': form, })

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
    try:
        cat_obj = DocumentCategory.objects.get_by_name(categories.fgos_category)
        documents = Document.objects.by_category(cat_obj)
    except DocumentCategory.DoesNotExist:
        documents = Document.objects.newest()
    pagination = miscellaneous.paginate(documents, request, key='document')
    return render(request, 'about_standards.html', {'title': u'Сведения об образовательной организации - образовательные стандарты', 'news': News.objects.all,
                                                    'year': timezone.now, 'docs': pagination,
                                                    'categories': DocumentCategory.objects.order_by_doc_count().all,
                                                    "cats": DocumentCategory.objects.get_top_X, "cat_name": categories.fgos_category, })


def about_structure(request):
    return render(request, 'about_structure.html', {"news": News.objects.all, 'year': timezone.now,
                                                    "cats": DocumentCategory.objects.get_top_X, })


def about_vacancies(request):
    return render(request, 'about_vacancies.html', {"news": News.objects.all, 'year': timezone.now,
                                                    "cats": DocumentCategory.objects.get_top_X, })

def about_doc_refs(request):
    return render(request, 'about_doc_refs.html', {"news": News.objects.all, 'year': timezone.now,
                                                    "cats": DocumentCategory.objects.get_top_X, })

def edu_work(request):
    return render(request, 'edu_work.html', {"news": News.objects.all, 'year': timezone.now,
                                             "cats": DocumentCategory.objects.get_top_X, })

def control_results(request):
    try:
        cat_obj = DocumentCategory.objects.get_by_name(categories.check_acts)
        documents = Document.objects.by_category(cat_obj)
    except DocumentCategory.DoesNotExist:
        documents = Document.objects.newest()
    pagination = miscellaneous.paginate(documents, request, key='document')
    return render(request, 'control_results.html', {'title': u'Сведения об образовательной организации - предписания органов, осуществляющих государственный контроль (надзор) в сфере образования, отчеты об исполнении таких предписаний', 'news': News.objects.all,
                                                    'year': timezone.now, 'docs': pagination,
                                                    'categories': DocumentCategory.objects.order_by_doc_count().all,
                                                    "cats": DocumentCategory.objects.get_top_X, "cat_name": categories.check_acts, })

def el_dist_study(request):
    return docs_by_cat_name(request, categories.el_dist_study)

def about_docs_all(request):
    return docs_by_cat_name(request, categories.about_docs_category)


def about_financial(request):
    return docs_by_cat_name(request, categories.financial_category)


def about_mto(request):
    return docs_by_cat_name(request, categories.mto_category)


def about_support(request):
    return docs_by_cat_name(request, categories.support_category)


def about_additional(request):
    return docs_by_cat_name(request, categories.paid_category)

def additional(request):
    return docs_by_cat_name(request, categories.additional_category)

def perf_control(request):
    return docs_by_cat_name(request, categories.perf_control)

def les_curriculum(request):
    return docs_by_cat_name(request, categories.les_curriculum)

def rp_annots(request):
    return docs_by_cat_name(request, categories.rp_annots)

def employment_rules(request):
    return docs_by_cat_name(request, categories.employment_rules)

def addsched(request):
    return docs_by_cat_name(request, categories.addsched)

def self_diagnosis(request):
    return docs_by_cat_name(request, categories.self_diagnosis_category)

def staff_doc(request):
    return docs_by_cat_name(request, categories.staff_list_category)


def educational_work(request):
    return docs_by_cat_name(request, categories.vosp_category)


def methodical(request):
    return docs_by_cat_name(request, categories.methodical_category)


def curriculum(request):
    return docs_by_cat_name(request, categories.curriculum_category)


def schedule(request):
    return docs_by_cat_name(request, categories.schedule_category)

def lessched(request):
    return docs_by_cat_name(request, categories.lessched)

def mealorg(request):
    return docs_by_cat_name(request, categories.mealorg)

def security(request):
    return docs_by_cat_name(request, categories.security)

def anticovid(request):
    return docs_by_cat_name(request, categories.anticovid)

def psychped(request):
    return docs_by_cat_name(request, categories.psychped)

def pedpsych(request):
    return docs_by_cat_name(request, categories.pedpsych)

def socped(request):
    return docs_by_cat_name(request, categories.socped)

def socservice(request):
    return docs_by_cat_name(request, categories.socservice)

def mediation(request):
    return docs_by_cat_name(request, categories.mediation)

def p500_docs(request):
    return docs_by_cat_name(request, categories.p500_plus)

def younguard(request):
    return docs_by_cat_name(request, categories.younguard)

def municipal_task(request):
    return docs_by_cat_name(request, categories.municipal_task_category)

def extras(request):
    return docs_by_cat_name(request, categories.extras_category)


def annotations(request):
    return docs_by_cat_name(request, categories.annotations_category)


def main_language(request):
    return docs_by_cat_name(request, categories.main_language_category)


def study(request):
    return docs_by_cat_name(request, categories.study_category)


def main_docs(request):
    return docs_by_cat_name(request, categories.main_docs_category)


def about_schedules(request):
    return docs_by_cat_name(request, categories.schedules_category)


def programs(request):
    return docs_by_cat_name(request, categories.programs_category)


def credentials(request):
    return docs_by_cat_name(request, categories.credits_category)

def olymp(request):
    return docs_by_cat_name(request, categories.olymp)

def curriculum(request):
    return docs_by_cat_name(request, categories.curriculum_category)


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

def enrollment(request):
    return docs_by_cat_name(request, categories.enrollment_category)

def vpk(request):
    return docs_by_cat_name(request, categories.vpk)

def museum(request):
    return docs_by_cat_name(request, categories.museum)

def heo_collab(request):
    return docs_by_cat_name(request, categories.heo_collab)

def org_collab(request):
    return docs_by_cat_name(request, categories.org_collab)

def prof_orient(request):
    return docs_by_cat_name(request, categories.prof_orient)

def studgov(request):
    return docs_by_cat_name(request, categories.studgov)

def school_press(request):
    return docs_by_cat_name(request, categories.press)

def projs(request):
    return docs_by_cat_name(request, categories.projs)

def sport(request):
    return docs_by_cat_name(request, categories.sport)

def parents(request):
    return docs_by_cat_name(request, categories.parents)

def heads(request):
    return docs_by_cat_name(request, categories.heads)

def fairs(request):
    return docs_by_cat_name(request, categories.fairs)

def vector(request):
    return docs_by_cat_name(request, categories.vector)

def project_victory(request):
    return docs_by_cat_name(request, categories.project_victory)

def yid(request):
    return docs_by_cat_name(request, categories.yid)

def rds(request):
    return docs_by_cat_name(request, categories.rds)

def sections(request):
    return docs_by_cat_name(request, categories.sections)

def spsections(request):
    return docs_by_cat_name(request, categories.spsections)

def sections_full(request):
    return docs_by_cat_name(request, categories.sections_full)

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
    return render(request, 'login.html', {'news': News.objects.all, 'year': timezone.now,
                                          'cats': DocumentCategory.objects.get_top_X, 'form': form, })


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


@login_required
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


@login_required
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
        model['category'] = staffer.category.title
        model['subject'] = staffer.subject.title
        form = StaffMemberForm(model)
    return render(request, 'staff_member_form_edit.html', {"news": News.objects.all, 'year': timezone.now,
                                                           "cats": DocumentCategory.objects.get_top_X,
                                                           "form": form, })


@login_required
def add_photo_certain(request, album_id):
    if not Album.objects.all:
        return HttpResponseRedirect(reverse('add_album'))
    if request.method == 'POST':
        form = PhotoAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if album_id:
                real_album_id = album_id
            else:
                real_album_id = form.cleaned_data['album'].title_id
            return HttpResponseRedirect(reverse('album', kwargs={'album_id': real_album_id, }))
        else:
            return HttpResponseRedirect(reverse('add_photo_certain', kwargs={'album_id': album_id, }))
    else:
        form = PhotoAddForm(album_id=album_id)
        return render(request, 'photo_add.html', {'news': News.objects.all, 'year': timezone.now,
                                                  'cats': DocumentCategory.objects.get_top_X,
                                                  'form': form, })


@login_required
def add_photo_choice(request):
    return add_photo_certain(request, None)


@login_required
def add_album(request):
    if request.method == 'POST':
        form = AlbumAddForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('albums_list'))
    else:
        form = AlbumAddForm()
        return render(request, 'album_add.html', {'news': News.objects.all, 'year': timezone.now,
                                                  'cats': DocumentCategory.objects.get_top_X,
                                                  'form': form, })


def albums_list(request):
    albums = Album.objects.queryset().all()
    return render(request, 'albums.html', {'news': News.objects.all, 'year': timezone.now,
                                           'cats': DocumentCategory.objects.get_top_X,
                                           'albums': albums, })


def album(request, album_id):
    try:
        album_entry = Album.objects.single(album_id)
        album_entry.views_count = album_entry.views_count + 1
        album_entry.save()
    except Album.DoesNotExist:
        raise Http404()
    return render(request, 'album.html', {'news': News.objects.all, 'year': timezone.now,
                                          'cats': DocumentCategory.objects.get_top_X,
                                          'album': album_entry, })

def el_journ(request):
    return render(request, 'el_journ.html', {'news': News.objects.all, 'year': timezone.now,
                                          'cats': DocumentCategory.objects.get_top_X, })

def feedback_site (request):
    return render(request, 'feedback.html', {"news": News.objects.all, 'year': timezone.now,
                                             "cats": DocumentCategory.objects.get_top_X,
                                             "top_news": News.objects.get_top_X, })

def feedback_ticket (request):
    return render(request, 'feedback_ticket.html', {"news": News.objects.all, 'year': timezone.now,
                                             "cats": DocumentCategory.objects.get_top_X,
                                             "top_news": News.objects.get_top_X, })

def feedback_query (request):
    return render(request, 'feedback_query.html', {"news": News.objects.all, 'year': timezone.now,
                                             "cats": DocumentCategory.objects.get_top_X,
                                             "top_news": News.objects.get_top_X, })

def feedback_faq(request):
    return render(request, 'faq.html', {"news": News.objects.all, 'year': timezone.now,
                                        "cats": DocumentCategory.objects.get_top_X,
                                        "top_news": News.objects.get_top_X, })

@login_required
def user_management(request):
    users = UrlUser.objects.all()
    for user in users:
        print(user)
    return render(request, 'users_list.html', {'news': News.objects.all, 'year': timezone.now,
                                               'cats': DocumentCategory.objects.get_top_X, 'users_list': users, })


@login_required
def edit_user(request, user):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            form.save(user)
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('user_management'))
            else:
                return HttpResponseRedirect(reverse('index'))
    else:
        user = model_to_dict(user)
        form = ProfileEditForm(user)
    return render(request, 'profile_edit.html', {'news': News.objects.all, 'year': timezone.now,
                                                 'cats': DocumentCategory.objects.get_top_X,
                                                 'form': form, 'user': user, })


@login_required
def edit(request):
    return edit_user(request, request.user)


@login_required
def edit_user_by_username(request, username):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('user_management'))
    try:
        user = UrlUser.objects.get_by_natural_key(username=username)
        return edit_user(request, user)
    except User.DoesNotExist:
        raise Http404()


@login_required
def delete_user(request, username):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('user_management'))
    try:
        user = UrlUser.objects.get_by_natural_key(username=username)
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('user_management'))
    except UrlUser.DoesNotExist:
        raise Http404()


@login_required
def logout(request):
    redirect = request.GET.get('continue', '/')
    auth.logout(request)
    return HttpResponseRedirect(redirect)


@login_required
def add_user(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('user_management'))
    if request.method == 'POST':
        form = UrlUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_management'))
    else:
        form = UrlUserCreationForm()
        return render(request, 'add_user.html', {'news': News.objects.all, 'year': timezone.now,
                                                 'cats': DocumentCategory.objects.get_top_X, 'form': form, })


def p500_main(request):
    return render(request, 'p500_main.html', {'news': News.objects.all, 'year': timezone.now,
                                              'cats': DocumentCategory.objects.get_top_X, })
