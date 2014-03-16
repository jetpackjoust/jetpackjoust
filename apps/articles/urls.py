from django.conf.urls import patterns, url

from articles import views


regex = {'list_articles_by_day':
         r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
         'show_article':
         r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)$'}


urlpatterns = patterns('',
                       url(r'^$',
                           views.ArticleListView.as_view(),
                           name='list_articles'),

                       url(r'tags/$',
                           views.TagListView.as_view(),
                           name='list_tags'),

                       url(r'tags/(?P<slug>[^/]+)$',
                           views.TagDetailView.as_view(),
                           name='show_tag'),

                       url(r'contributors/$',
                           views.AuthorListView.as_view(),
                           name='list_contributors'),

                       url(r'contributors/(?P<slug>[^/]+)$',
                           views.AuthorDetailView.as_view(),
                           name='show_contributor'),

                       url(r'(?P<year>\d{4})/$',
                           views.ArticleListView.as_view(),
                           name='list_articles_by_year'),

                       url(r'(?P<year>\d{4})/(?P<month>\d{2})/$',
                           views.ArticleListView.as_view(),
                           name='list_articles_by_month'),

                       url(regex['list_articles_by_day'],
                           views.ArticleListView.as_view(),
                           name='list_articles_by_day'),

                       url(regex['show_article'],
                           views.ArticleDetailView.as_view(),
                           name='show_article'),)
