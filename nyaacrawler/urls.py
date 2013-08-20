from django.conf.urls import patterns, url

from nyaacrawler.views import index, save_subscription

urlpatterns = patterns('',
    url(r'^subscription/$', save_subscription),
    url(r'^$', index),
)
