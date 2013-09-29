from django.contrib import admin
from django.template.response import TemplateResponse
from nyaacrawler import models
from nyaacrawler.utils.webcrawler import crawl_specific_anime

class AliasNamesInline(admin.StackedInline):
    model = models.AnimeAlias
    fk_name = 'anime'
    fields = ('title',)
    
class TorrentsInline(admin.StackedInline):
    model = models.Torrent
    fk_name = 'title'
    fields = ('torrent_name',)

class IsKnownFilter(admin.SimpleListFilter):
    """
    Filters known and unknown alias names
    """
    title = 'belongs to anime'

    parameter_name = 'known'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', ('Known anime')),
            ('no', ('unKnown anime')),
        )
    def queryset(self,request,queryset):
        if self.value() == "yes":
            return queryset.exclude(anime__official_title=models.Anime.UNKNOWN_ANIME)

        if self.value() == "no":
            return queryset.filter(anime__official_title=models.Anime.UNKNOWN_ANIME)
    
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('official_title', 'image')
    search_fields = ('official_title',)

    inlines = [
        AliasNamesInline
    ]
    
class AnimeAliasAdmin(admin.ModelAdmin):
    list_display = ('title', 'anime', 'do_initialize', 'is_initialized')
    search_fields = ('title',)
    readonly_fields = ('is_initialized',)

    inlines = [
        TorrentsInline
    ]

    list_filter = (IsKnownFilter,)
    
    def migrate_selected(self, request, queryset):
    # Action which changes the selected AnimeAlias' anime foreignkey.

        if request.POST.get('newOfficialAnimeName'):
            rows_migrated = queryset.update(
                anime = models.Anime.objects.get(
                official_title=str(
                request.POST.get('newOfficialAnimeName')
            )))

            for anime_alias in queryset:
                if not anime_alias.is_initialized:
                    anime_alias.do_initialize = True
                    anime_alias.save()

            if rows_migrated:
                message_bit = "Anime Alias' Anime pointer updated."
            else:
                message_bit = "No Alias modified."

            self.message_user(request, message_bit)
            return None

        context = {
            "title"         :   "Pending Migration",
            "migrateable_objects"   :   [queryset],
            "queryset"      :   queryset,
            "animeNames"    :   [name.official_title for name in models.Anime.objects.all()],
            "objects_name"  :   self.model._meta.verbose_name,
            "opts"          :   self.model._meta,
            "app_label"     :   self.model._meta.app_label,
        }

        # Display the confirmation page
        return TemplateResponse(request, ["anime_alias_migration.html"],
            context, current_app=self.admin_site.name)

    migrate_selected.short_description = "Migrate selected Anime Alias to another Anime"
    actions = [migrate_selected]

class TorrentAdmin(admin.ModelAdmin):
    list_display = ('title', 'episode','fansub', 'quality', 'infoHash')
    search_fields = ('torrent_name', 'fansub', 'quality')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'anime')

admin.site.register(models.Anime, AnimeAdmin)

admin.site.register(models.AnimeAlias, AnimeAliasAdmin)

admin.site.register(models.Torrent, TorrentAdmin)

admin.site.register(models.Subscription, SubscriptionAdmin)
