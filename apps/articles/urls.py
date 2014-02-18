from django.conf.urls import patterns, include, url

from articles import views

urlpatterns = patterns('',
    url(r'^$', views.ArticleListView.as_view(), name='index'),

    url(r'tags/$', views.TagListView.as_view(), name='index_tags'),

    url(r'tags/(?P<tag_slug>[^/]+)$', views.TagDetailView.as_view(), name='show_tag'),

    url(r'contributors/$', views.AuthorListView.as_view(),
        name='index_contributors'),

    url(r'contributors/(?P<contributor_slug>[^/]+)$',
        views.AuthorDetailView.as_view(), name='show_contributor'),

    url(r'(?P<year>\d{4})/$', views.ArticleListView.as_view(),
        name='by_year'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/$', views.ArticleListView.as_view(),
        name='by_month'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.ArticleListView.as_view(), name='by_day'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)$',
        views.ArticleDetailView.as_view(), name='show_article'),

                       )
