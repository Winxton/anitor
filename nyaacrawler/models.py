from django.db import models
from django.db.models.aggregates import Max
from django.db.models import Q
from django.contrib.contenttypes import generic
from django.forms import ModelForm

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

import os
# Create your models here.

class Anime(models.Model):
    UNKNOWN_ANIME = 'unknown-anime-placeholder'

    """
    The official anime 'entity'
    """
    official_title = models.CharField(max_length=200)
    image = models.URLField(blank=True)

    def __unicode__(self):
        return self.official_title
    def latest_episodes(self):
        return Torrent.objects.filter(
            episode=self.current_episode(),
            title__anime=self
            )
    def current_episode(self):
        #ex: ["max_episode" : num]
        episode = Torrent.objects.filter(
                title__anime=self
            ).aggregate(
                max_episode=Max('episode')
            )['max_episode']
        return 0 if episode is None else episode

class AnimeAlias(models.Model):
    """
    Anime name given by the fansub group.
    Used because an anime can have multiple names
    """
    anime = models.ForeignKey(Anime, related_name="anime_aliases")
    title = models.CharField(max_length=200)
    confirmed = models.BooleanField()

    def __unicode__(self):
        return self.title

class Torrent(models.Model):
    title = models.ForeignKey(AnimeAlias, related_name='torrents')
    torrent_name = models.CharField(max_length=200)
    episode = models.FloatField()
    fansub = models.CharField(max_length=30)
    quality = models.CharField(max_length=10)
    url = models.URLField()
    infoHash = models.CharField(max_length=40, null=True)
    vidFormat = models.CharField(max_length=10)
    published = models.BooleanField(default=True)
    seeders = models.PositiveIntegerField()
    leechers = models.PositiveIntegerField()

    def __unicode__(self):
        return self.title.anime.official_title
    def get_matching_subscriptions(self):
        return self.anime.subscriptions.filter(
            Q (qualities__contains=(self.quality)) | Q(qualities='all'),
            Q (fansubs__contains=(self.fansub)) | Q(fansubs='all'),
            Q (current_episode=self.episode-1)
        )

class User(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    
    #used if first subscribed and not registered
    subscription_activation_key = models.CharField(
        max_length=32,
        default=os.urandom(16).encode('hex')
    )
    
    #used when user is registered
    registration_activation_key = models.CharField(
        max_length=32,
        default=os.urandom(16).encode('hex')
    )
    #user has been validated
    confirmed_subscription = models.BooleanField()
    #user is registered
    confirmed_registered = models.BooleanField()

    def __unicode__(self):
        return self.email
    def set_activated(self):
        self.confirmed_subscription = True
    def set_registered(self):
        self.confirmed_registered = True
    def has_no_subscriptions(self):
        return self.get_num_subscriptions() == 0
    def get_num_subscriptions(self):
        return self.subscriptions.count()
    
class Subscription(models.Model):
    user = models.ForeignKey(User, related_name="subscriptions")
    anime = models.ForeignKey(Anime, related_name="subscriptions")
    current_episode = models.FloatField()
    qualities = models.CharField(max_length=30)
    fansubs = models.CharField(max_length=250)
    unsubscribe_key = models.CharField(
        max_length=32,
        default=os.urandom(16).encode('hex')
    )

    def __unicode__(self):
        return self.user.email+" - "+self.anime.official_title
    def get_email(self):
        return self.user.email
    def increment_episode(self):
        self.current_episode += 1

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']