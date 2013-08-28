from django.conf.urls import patterns, url

from nyaacrawler.views import *

urlpatterns = patterns('',
    url(r'^subscribe/$', subscribe),
    url(r'^unsubscribe/(?P<unsubscribe_key>\w+)/$', unsubscribe),
    url(r'^search/get-anime-list/$', get_anime_list, name="animeList"),
    url(r'^$', index),
)
