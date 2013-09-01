from django.conf.urls import patterns, include, url

from articles import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'tags/', views.index_tags, name='index_tags'),

    url(r'tags/(?P<tag_slug>[^/]+)$', views.show_tag, name='show_tag'),

    url(r'(?P<year>\d{4})/$', views.index_by_year, name='by_year'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/$', views.index_by_month,
        name='by_month'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.index_by_day, name='by_day'),

    url(r'\d{4}/\d{2}/\d{2}/(?P<slug>[^/]+)$',
        views.show_article, name='show_article'),

                       )
