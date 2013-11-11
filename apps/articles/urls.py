from django.conf.urls import patterns, include, url

from articles import views

urlpatterns = patterns('',
    url(r'^$', views.index_articles, name='index'),

    url(r'tags/$', views.index_tags, name='index_tags'),

    url(r'tags/(?P<tag_slug>[^/]+)$', views.show_tag, name='show_tag'),

    url(r'contributors/$', views.index_contributors,
        name='index_contributors'),

    url(r'contributors/(?P<contributor_slug>[^/]+)$', views.show_contributor,
        name='show_contributor'),

    url(r'(?P<year>\d{4})/$', views.index_articles, name='by_year'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/$', views.index_articles,
        name='by_month'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.index_articles, name='by_day'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)$',
        views.show_article, name='show_article'),

                       )
