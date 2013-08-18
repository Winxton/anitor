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
	def __unicode__(self):
		return self.torrent_name

class User(models.Model):
	email = models.EmailField()
	created = models.DateTimeField(auto_now_add=True)
	activation_key = models.CharField(max_length=30)
	def __unicode__(self):
		return self.email

class Subscription(models.Model):
	user = models.ForeignKey(User)
	anime = models.ForeignKey(Anime)
	current_episode = models.FloatField()
	qualities = models.CharField(max_length=30)
	sub_groups = models.CharField(max_length=80)
