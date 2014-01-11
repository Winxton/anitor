from django.core.management.base import BaseCommand, make_option
from nyaacrawler.utils.webcrawler import create_new_season_list

class Command(BaseCommand):

	args = '<season>'
	help = 'Crawl seasonal anime chart for new upcoming Anime.'

	def handle(self, *args, **options):
		
		if len(args) == 0:
			create_new_season_list()
		else:
			create_new_season_list(args[0])
