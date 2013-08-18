from django.contrib import admin
from nyaacrawler import models

class AnimeAdmin(admin.ModelAdmin):
	list_display = ('identifier','title')

class AnimeAliasAdmin(admin.ModelAdmin):
    list_display = ('alias_name', "anime")

class TorrentAdmin(admin.ModelAdmin):
    list_display = ('episode','fansub')

class UserAdmin(admin.ModelAdmin):
	list_display = ('email','created')

class SubscriptionAdmin(admin.ModelAdmin):
	list_display = ('user', 'anime')

admin.site.register(models.Anime, AnimeAdmin)

admin.site.register(models.AnimeAlias, AnimeAliasAdmin)

admin.site.register(models.Torrent, TorrentAdmin)

admin.site.register(models.User, UserAdmin)

admin.site.register(models.Subscription, SubscriptionAdmin)