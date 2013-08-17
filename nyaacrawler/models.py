from django.db import models
from django.db.models.aggregates import Max
# Create your models here.

class Anime(models.Model):
	identifier = models.IntegerField()
	title = models.CharField(max_length=200)

	def __unicode__(self):
		return self.title
	def latest_episodes(self):
		return self.torrents.all().filter(episode=self.current_episode()['max_episode'])
	def current_episode(self):
		return self.torrents.aggregate(max_episode=Max('episode'))

class AnimeAlias(models.Model):
	anime = models.ForeignKey(Anime, related_name="animeAliases")
	aliasName = models.CharField(max_length=200)

class Torrent(models.Model):
	anime = models.ForeignKey(Anime, related_name='torrents')
	torrentName = models.CharField(max_length=200)
	episode = models.FloatField()
	fansub = models.CharField(max_length=30)
	quality = models.CharField(max_length=10)
	url = models.URLField()
	tracker = models.CharField(max_length=40)
	infoHash = models.CharField(max_length=30)
	vidFormat = models.CharField(max_length=10)
