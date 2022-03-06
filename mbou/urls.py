from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect

from mbou import views, settings

urlpatterns = [
    url(r'^$', views.index, name='start_page'),
    url(r'^index/$', views.index, name="index"),
    url(r'^base/$', views.base, name="base"),

    url(r'^logout/$', views.logout, name="logout"),
    url(r'^edit/$', views.edit, name="profile-edit"),

    url(r'^news/(?P<id>\d+)/?$', views.news, name="news"),
    url(r'^news/add/$', views.news_add, name="add_news"),

    url(r'^lessons/edit/$', views.lesson_edit, name="edit_lesson"),
    url(r'^lessons/show/$', views.lessons_show, name="lessons_show"),

    url(r'^documents/add/$', views.document_add, name="document_add"),
    url(r'^documents/(?P<title>.+)/', views.document_show, name="document_show"),
    url(r'^docs-newest/$', views.docs_newest, name="docs_newest"),
    url(r'^docs-category/(?P<cat_name>.+)/$', views.docs_by_category, name="docs_by_category"),
    url(r'^docs-search/$', views.docs_search, name="docs_search"),
    url(r'^docs-search/(?P<query>.+)/$', views.docs_search_result, name="docs_search_result"),

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
    url(r'^about/schedule/$', views.schedule, name="schedule"),
    url(r'^about/doc_refs/$', views.about_doc_refs, name="about_doc_refs"),
    url(r'^municipal_task/$', views.municipal_task, name="municipal_task"),
    url(r'^extras/$', views.extras, name="extras"),
    url(r'^main_docs/$', views.main_docs, name="main_docs"),
    url(r'^curriculum/$', views.curriculum, name="curriculum"),
    url(r'^study/$', views.study, name="study"),
    url(r'^performance_control/$', views.perf_control, name='perf_control'),
    url(r'^lessons_curriculum/$', views.les_curriculum, name='les_curriculum'),
    url(r'^employment_rules/$', views.employment_rules, name='employment_rules'),
    url(r'^control_results/$', views.control_results, name="control_results"),
    url(r'^rp_annots/$', views.rp_annots, name="rp_annots"),
    url(r'^el_dist_study/$', views.el_dist_study, name="el_dist_study"),

    url(r'^enrollment/$', views.enrollment, name="enrollment"),

    url(r'^photos/$', views.photos, name="photos"),

    url(r'^annotations/$', views.annotations, name="annotations"),

    url(r'^feedback/site/$', views.feedback_site, name="feedback_site"),
    url(r'^feedback/ticket/$', views.feedback_ticket, name="feedback_ticket"),
    url(r'^feedback/faq/$', views.feedback_faq, name="feedback_faq"),
    url(r'^feedback/query/$', views.feedback_query, name="feedback_query"),

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
    url(r'^useful-links/$', views.external_links, name="external_links"),
    url(r'^self-diagnosis/$', views.self_diagnosis, name="self_diagnosis"),
    url(r'^vpk/$', views.vpk, name='vpk'),
    url(r'^studgov/$', views.studgov, name='studgov'),
    url(r'^el_journ/$', views.el_journ, name='el_journ'),
    url(r'^school_press/$', views.school_press, name='school_press'),
    url(r'^museum/$', views.museum, name='museum'),
    url(r'^heo_collab/$', views.heo_collab, name='heo_collab'),
    url(r'^org_collab/$', views.org_collab, name='org_collab'),
    url(r'^prof_orient/$', views.prof_orient, name='prof_orient'),
    url(r'^olymp/$', views.olymp, name='olymp'),
    url(r'^projects/$', views.projs, name='projects'),
    url(r'^sport/$', views.sport, name='sport'),
    url(r'^lessched/$', views.lessched, name='lessched'),
    url(r'^mealorg/$', views.mealorg, name='mealorg'),
    url(r'^security/$', views.security, name='security'),
    url(r'^anticovid/$', views.anticovid, name='anticovid'),
    url(r'^parents/$', views.parents, name='parents'),
    url(r'^fairs/$', views.fairs, name='fairs'),
    url(r'^parents/$', views.parents, name='parents'),
    url(r'^heads/$', views.heads, name='heads'),
    url(r'^vector/$', views.vector, name='vector'),
    url(r'^project_victory/$', views.project_victory, name='project_victory'),
    url(r'^edu_work/$', views.edu_work, name='edu_work'),
    url(r'^additional/$', views.additional, name='additional'),
    url(r'^addsched/$', views.addsched, name='addsched'),
    url(r'^yid/$', views.yid, name='yid'),
    url(r'^rds/$', views.rds, name='rds'),
    url(r'^sections/$', views.sections, name='sections'),
    url(r'^spsections/$', views.spsections, name='spsections'),
    url(r'^full_sections/$', views.sections_full, name='sections_full'),
    url(r'^younguard/$', views.younguard, name='younguard'),
    url(r'^psychped/$', views.psychped, name='psychped'),
    url(r'^pedpsych/$', views.pedpsych, name='pedpsych'),
    url(r'^socped/$', views.socped, name='socped'),
    url(r'^socservice/$', views.socservice, name='socservice'),
    url(r'^mediation/$', views.mediation, name='mediation'),

    url(r'^food/add/$', views.food_table_add, name='food_table_add'),
    url(r'^food/table/(?P<name>.+)/$', views.food_table_show, name='food_table_show'),
    url(r'^food/(?P<name>.+)/$', views.food_table_get, name='food_table_get'),
    url(r'^food/$', views.food_table_list, name='food_table_list'),

    url(r'^staff/all/$', views.staff_list_all, name="staff_all"),
    url(r'^staff/admin/$', views.staff_list_admin, name="staff_admin"),
    url(r'^staff/elementary/$', views.staff_list_elementary, name="staff_elementary"),
    url(r'^staff/subjects/$', views.staff_list_not_elementary, name="staff_not_elementary"),
    url(r'^staff/add/$', views.staff_member_add, name="add_staff_member"),
    url(r'^staff/edit/(?P<full_name>.+)/$', views.staff_member_edit, name="edit_staff_member"),
    url(r'^staff/list-doc/$', views.staff_doc, name="staff_doc"),

    url(r'^albums/$', views.albums_list, name="albums_list"),
    url(r'^albums/add/$', views.add_album, name="add_album"),
    url(r'^albums/photos/(?P<album_id>.+)/$', views.album, name="album"),

    url(r'^photos/add/$', views.add_photo_choice, name="add_photo_choice"),
    url(r'^photos/add/(?P<album_id>.+)/$', views.add_photo_certain, name="add_photo_certain"),

    url(r'^users-list/$', views.user_management, name="user_management"),
    url(r'^users/add/$', views.add_user, name="add_user"),
    url(r'^users/edit/(?P<username>.+)/$', views.edit_user_by_username, name="profile_edit_super"),
    url(r'^users/delete/(?P<username>.+)/$', views.delete_user, name="profile_delete"),
    url(r'^staff/login/$', views.login, name="login"),

    url(r'^p500/main/$', views.p500_main, name="p500_main"),
    url(r'^p500/docs/$', views.p500_docs, name="p500_docs"),

    url(r'^admin/', admin.site.urls, name=admin),
    #url(r'^favicon.ico/$', lambda ans: HttpResponseRedirect(settings.MEDIA_URL+'pics/favicon.png')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
