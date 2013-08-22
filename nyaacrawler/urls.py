from django.conf.urls import patterns, url

from nyaacrawler.views import index, save_subscription, get_anime_list

urlpatterns = patterns('',
    url(r'^subscription/$', save_subscription),
    url(r'^search/get-anime-list/$', get_anime_list, name="animeList"),
    url(r'^$', index),
)
