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
        return 0 if episode is None else int(episode)
        
    @classmethod
    def get_unknown_placeholder(cls):
        unknown_placeholder = cls.objects.get(official_title=Anime.UNKNOWN_ANIME)
        return unknown_placeholder

    @classmethod
    def get_active_anime(cls):
        return Anime.objects.filter(anime_aliases__torrents__isnull=False).distinct()
    
    @classmethod
    def get_active_anime_by_leechers(cls):
        result = Anime.objects.raw(
             "SELECT nyaacrawler_anime.*, anime_seeders "
            + "FROM nyaacrawler_anime "
            + "INNER JOIN "
                +"(SELECT animealiases.anime_id, sum(animealiases.alias_seeders) as anime_seeders "
                    + "FROM"
                        + "(SELECT nyaacrawler_animealias.*, sum(nyaacrawler_torrent.seeders) as alias_seeders "
                        + "FROM nyaacrawler_animealias "
                        + "INNER JOIN nyaacrawler_torrent "
                        + "ON nyaacrawler_torrent.title_id = nyaacrawler_animealias.id "
                        + "GROUP by nyaacrawler_torrent.title_id) animealiases "
                + "GROUP BY animealiases.anime_id) combined_alias "
            + "ON nyaacrawler_anime.id=combined_alias.anime_id "
            + "WHERE anime_seeders>0 "
            + "ORDER BY anime_seeders DESC "
            )
        print result
        return result


    def save(self, *args, **kwargs):
        from nyaacrawler.utils import MyAnimeList 
        if not self.image:
            self.image = MyAnimeList.get_anime_image_url(self.official_title)
        super(Anime, self).save()

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
        return self.title.anime.subscriptions.filter(
            Q (qualities__contains=(self.quality)) | Q(qualities='all'),
            Q (fansubs__contains=(self.fansub)) | Q(fansubs='all'),
            Q (current_episode=int(self.episode)-1)
        )
        
class Subscription(models.Model):
    email = models.EmailField()
    anime = models.ForeignKey(Anime, related_name="subscriptions")
    current_episode = models.FloatField()
    qualities = models.CharField(max_length=30)
    fansubs = models.CharField(max_length=250)
    unsubscribe_key = models.CharField(
        max_length=32,
        default=os.urandom(16).encode('hex')
    )
    
    def __unicode__(self):
        return self.email+" - "+self.anime.official_title
    @classmethod
    def get_subscriptions_for_email(cls, email):
        return Subscription.objects.filter(email=email)
    def get_email(self):
        return self.email
    def increment_episode(self):
        self.current_episode += 1
    def get_unsubscribe_key(self):
        return self.unsubscribe_key

class SubscriptionForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ['email','anime','current_episode','qualities','fansubs']
