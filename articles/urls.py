from django.conf.urls import patterns, include, url

from articles import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    url(r'(?P<year>\d{4})/$', views.archive_by_year, name='by_year'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/$', views.archive_by_month,
        name='by_month'),

    url(r'(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        views.archive_by_day, name='by_day'),
                       )
