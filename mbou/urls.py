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
    url(r'^documents/(?P<title>.+)/', views.document_show, name = "document_show"),
    url(r'^docs-newest/$', views.docs_newest, name="docs_newest"),
    url(r'^docs-category/(?P<cat_name>.+)/', views.docs_by_category, name="docs_by_category"),

    url(r'^admin/', admin.site.urls, name=admin),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
