from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from mbou import views, settings

urlpatterns = [
    url(r'^$', views.index, name='start_page'),
    url(r'^index/', views.index, name="index"),
    url(r'^base/', views.base, name="base"),

    url(r'^mbou7-staff-login/', views.login, name="login"),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^edit/', views.edit, name="profile-edit"),

    url(r'^news/(?P<id>\d+)/?$', views.news, name="news"),
    url(r'^news/add/$', views.news_add, name="add_news"),

    url(r'^lessons/edit/$', views.lesson_edit, name="edit_lesson"),
    url(r'^lessons/show/$', views.lessons_show, name="lessons_show"),

    url(r'^documents/add/$', views.document_add, name="document_add"),
    url(r'^documents/(?P<title>.+)/', views.document_show, name="document_show"),
    url(r'^docs-newest/$', views.docs_newest, name="docs_newest"),
    url(r'^docs-category/(?P<cat_name>.+)/', views.docs_by_category, name="docs_by_category"),

    url(r'^about/main/$', views.about_main, name="about_main"),
    url(r'^about/docs/$', views.about_docs_all, name="about_docs"),
    url(r'^about/general/$', views.about_general, name="about_general"),
    url(r'^about/education/$', views.about_education, name="about_education"),
    url(r'^about/staff/$', views.about_staff, name="about_staff"),
    url(r'^about/standards/$', views.about_standards, name="about_standards"),
    url(r'^about/structure/$', views.about_structure, name="about_structure"),
    url(r'^about/vacancies/$', views.about_vacancies, name="about_vacancies"),
    url(r'^about/financial/$', views.about_financial, name="about_financial"),
    url(r'^about/mto/$', views.about_mto, name="about_mto"),
    url(r'^about/support/$', views.about_support, name="about_support"),
    url(r'^about/additional/$', views.about_additional, name="about_additional"),
    url(r'^about/main_language/$', views.main_language, name="about_language"),
    url(r'^about/schedules/$', views.about_schedules, name="about_schedules"),

    url(r'^photos/$', views.photos, name="photos"),

    url(r'^annotations/$', views.annotations, name="annotations"),

    url(r'^educational_work/$', views.educational_work, name="educational_work"),
    url(r'^methodical_work/$', views.methodical, name="methodical_work"),
    url(r'^educational_programs/$', views.programs, name="educational_programs"),
    url(r'^credentials/$', views.credentials, name="credentials"),
    url(r'^council/$', views.council, name="council"),
    url(r'^vacancies/$', views.vacancies, name="vacancies_docs"),
    url(r'^additional_education/$', views.about_additional, name="additional_education"),
    url(r'^regional_contests/$', views.regional_contests, name="regional_contests"),
    url(r'^school_standard/$', views.school_standard, name="school_standard"),
    url(r'^curriculum/$', views.curriculum, name="curriculum"),

    url(r'^staff/all/$', views.staff_list_all, name="staff_all"),
    url(r'^staff/admin/$', views.staff_list_admin, name="staff_admin"),
    url(r'^staff/elementary/$', views.staff_list_elementary, name="staff_elementary"),
    url(r'^staff/subjects/$', views.staff_list_not_elementary, name="staff_not_elementary"),
    url(r'^staff/add/$', views.staff_member_add, name="add_staff_member"),
    url(r'^staff/edit/(?P<full_name>.+)/', views.staff_member_edit, name="edit_staff_member"),

    url(r'^albums/$', views.albums_list, name="albums_list"),
    url(r'^albums/?P<album_id>.+/', views.album, name="album"),
    url(r'^albums/add/$', views.add_album, name="add_album"),

    url(r'photos/add/$', views.add_photo_choice, name="add_photo_choice"),
    url(r'photos/add/?P<album_id>.+/', views.add_photo_certain, name="add_photo_certain"),

    url(r'^admin/', admin.site.urls, name=admin),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
