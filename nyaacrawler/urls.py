from django.conf.urls import patterns, url
import nyaacrawler.views

urlpatterns = patterns('',
    url(r'^$', nyaacrawler.views.index)
)
