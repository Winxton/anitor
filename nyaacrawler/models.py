from django.db import models
from django.db.models.aggregates import Max
from django.db.models import Q
from django.contrib.contenttypes import generic
from django.forms import ModelForm

import os
# Create your models here.

class Anime(models.Model):
    """
    The official anime 'entity'
    """
    UNKNOWN_ANIME = 'unknown-anime-placeholder'

    official_title = models.CharField(max_length=200, unique=True)
    image = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return self.official_title

    def latest_episodes(self):
        return Torrent.objects.filter(
            episode=self.current_episode(),
            title__anime=self
            )

    def current_episode(self):
        episode = Torrent.objects.filter(
                title__anime=self
            ).aggregate(
                max_episode=Max('episode')
            )['max_episode']
        return 0 if episode is None else episode
        
    @classmethod
    def get_unknown_placeholder(cls):
        unknown_placeholder = cls.objects.get(official_title=Anime.UNKNOWN_ANIME)
        return unknown_placeholder
        
    @classmethod
    def get_active_anime(cls):
        return Anime.objects.filter(anime_aliases__torrents__isnull=False).distinct()
    
    """
    Myanimelist is down :(

    def save(self, *args, **kwargs):
        from nyaacrawler.utils import MyAnimeList 
        if not self.image:
            self.image = MyAnimeList.get_anime_image_url(self.official_title)
        super(Anime, self).save()
    """

class AnimeAlias(models.Model):
    """
    Anime name given by the fansub group.
    Used because an anime can have multiple names
    """
    anime = models.ForeignKey(Anime, related_name="anime_aliases")
    title = models.CharField(max_length=200, unique=True)
    #whether an initialization has been done already
    is_initialized = models.BooleanField(default=False)
    #whether an initialization needs to be done
    do_initialize = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def set_initialized(self):
        self.do_initialize = False
        self.is_initialized = True

class Torrent(models.Model):
    title = models.ForeignKey(AnimeAlias, related_name='torrents')
    torrent_name = models.CharField(max_length=200)
    episode = models.FloatField()
    fansub = models.CharField(max_length=30)
    quality = models.CharField(max_length=10)
    url = models.URLField()
    infoHash = models.CharField(max_length=40, null=True)
    vidFormat = models.CharField(max_length=10)
    seeders = models.PositiveIntegerField()
    leechers = models.PositiveIntegerField()
    file_size = models.CharField(max_length=15)

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
    def __unicode__(self):
        return self.user.email+" - "+self.anime.official_title

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['email']
