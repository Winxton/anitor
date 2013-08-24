from django.db import models
from django.db.models.aggregates import Max
from django.db.models import Q
from django.contrib.contenttypes import generic

# Create your models here.

class Anime(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(blank=True)
    desc = models.TextField()
    init = models.BooleanField()
    def __unicode__(self):
    	return self.title
    def latest_episodes(self):
    	return self.torrents.all().filter(episode=self.current_episode()['max_episode'])
    def current_episode(self):
    	#ex: ["max_episode" : num]
    	return self.torrents.aggregate(max_episode=Max('episode'))

class AnimeAlias(models.Model):
    anime = models.ForeignKey(Anime, related_name="animeAliases")
    alias_name = models.CharField(max_length=200)
    def __unicode__(self):
    	return self.alias_name

class Torrent(models.Model):
    anime = models.ForeignKey(Anime, related_name='torrents')
    torrent_name = models.CharField(max_length=200)
    episode = models.FloatField()
    fansub = models.CharField(max_length=30)
    quality = models.CharField(max_length=10)
    url = models.URLField()
    tracker = models.CharField(max_length=40)
    infoHash = models.CharField(max_length=30)
    vidFormat = models.CharField(max_length=10)
    published = models.BooleanField(default=True)
    def __unicode__(self):
        return self.anime.title
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
        max_length=30,
        blank = True
    )
    
    #used when user is registered
    registration_activation_key = models.CharField(
        max_length=30,
        blank = True
    )

    confirmed_registered = models.BooleanField()
    confirmed_subscription = models.BooleanField()
    def __unicode__(self):
        return self.email

    def set_activated(self):
        self.confirmed_subscription = True

    def set_registered(self):
        self.confirmed_registered = True

class Subscription(models.Model):
    user = models.ForeignKey(User, related_name="subscriptions")
    anime = models.ForeignKey(Anime, related_name="subscriptions")
    current_episode = models.FloatField()
    qualities = models.CharField(max_length=30)
    fansubs = models.CharField(max_length=250)
    def get_email(self):
        return self.user.email
    def increment_episode(self):
        self.current_episode += 1
    def __unicode__(self):
        return self.user.email+" - "+self.anime.title
