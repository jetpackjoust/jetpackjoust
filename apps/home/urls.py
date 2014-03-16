from django.conf.urls import patterns, url

from home.views import HomeView

urlpatterns = patterns('',
                       url(r'^$', HomeView.as_view(), name="HomeView"),)
