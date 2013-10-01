from django.core.management.base import NoArgsCommand, make_option
from nyaacrawler.utils.webcrawler import crawl_anime, crawl_specific_anime
from nyaacrawler.models import AnimeAlias

class Command(NoArgsCommand):

	help = 'Does an initial crawl on all the anime which has the \'do_initialize\' flag as true'

	def handle_noargs(self, **options):

		#all anime which needs to be initialized
		anime_to_initialize = AnimeAlias.objects.filter(do_initialize=True)

		for anime in anime_to_initialize:
			crawl_specific_anime(anime.title)
			anime.set_initialized()
			anime.save()