from django.core.management.base import NoArgsCommand, make_option

from nyaacrawler.utils.webcrawler import crawl_anime

class Command(NoArgsCommand):

	help = "Crawls anime from the front page of nyaa.se. Runs periodically as a cron job"

	def handle_noargs(self, **options):
		crawl_anime()
