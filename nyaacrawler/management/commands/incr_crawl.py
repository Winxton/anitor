from django.core.management.base import BaseCommand, make_option

from nyaacrawler.utils.webcrawler import crawl_anime, crawl_specific_anime

class Command(BaseCommand):

	args = '<anime_name>'
	help = 'Crawls anime from the front page of nyaa.se if no arguments are given. \
			Otherwise, crawls using the search function for a specific anime. Runs periodically as a cron job'

	def handle(self, *args, **options):
		
		if len(args) == 0:
			crawl_anime()

		else:
			for anime_name in args:				
				crawl_specific_anime(anime_name)

