from django.conf.urls import patterns, url

from nyaacrawler.views import *

urlpatterns = patterns('',
    url(r'^subscribe/$', subscribe),
    url(r'^unsubscribe/(?P<unsubscribe_key>\w+)/$', unsubscribe),
    url(r'^search/get-torrent-list/$', get_torrents_for_anime_episode),
    url(r'^confirm-subscription/(?P<subscription_activation_key>\w+)/$', confirm_email),
    url(r'^$', index),
)
