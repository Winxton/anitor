from django.contrib import admin
from nyaacrawler import models

class AnimeAdmin(admin.ModelAdmin):
	list_display = ('identifier','title')
class AnimeAliasAdmin(admin.ModelAdmin):
    list_display = ('aliasName', "anime")
class TorrentAdmin(admin.ModelAdmin):
    list_display = ('episode','fansub')
    
admin.site.register(models.Anime, AnimeAdmin)

admin.site.register(models.AnimeAlias, AnimeAliasAdmin)

admin.site.register(models.Torrent, TorrentAdmin)
