from django.contrib import admin
from django.template.response import TemplateResponse
from nyaacrawler import models
from nyaacrawler.utils.webcrawler import crawl_specific_anime

class AliasNamesInline(admin.StackedInline):
    model = models.AnimeAlias
    fk_name = 'anime'

class AnimeAdmin(admin.ModelAdmin):
    list_display = ('official_title',)
    search_fields = ('official_title',)

    inlines = [
        AliasNamesInline
    ]

class AnimeAliasAdmin(admin.ModelAdmin):
    list_display = ('anime', 'title', 'accepted')
    search_fields = ('title',)

    def migrate_selected(self, request, queryset):
    # Action which changes the selected AnimeAlias' anime foreignkey.

        if request.POST.get('newOfficialAnimeName'):
            rows_migrated = queryset.update(
                anime = models.Anime.objects.get(
                official_title=str(
                request.POST.get('newOfficialAnimeName')
            )))

            for anime_alias in queryset:
                if not anime_alias.accepted:
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

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','created')

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'anime')

admin.site.register(models.Anime, AnimeAdmin)

admin.site.register(models.AnimeAlias, AnimeAliasAdmin)

admin.site.register(models.Torrent, TorrentAdmin)

admin.site.register(models.User, UserAdmin)

admin.site.register(models.Subscription, SubscriptionAdmin)
