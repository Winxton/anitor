from django.core.management.base import BaseCommand, make_option
from nyaacrawler.utils.webcrawler import crawl_season_list

class Command(BaseCommand):

	args = '<season>'
	help = 'Crawl seasonal anime chart for new upcoming Anime'

	def handle(self, *args, **options):
		
		if len(args) == 0:
			crawl_season_list()
		else:
			crawl_season_list(args[0])
