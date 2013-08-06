from django.conf.urls import patterns, include, url

from home.views import HomeView

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name="HomeView"),
                       )
