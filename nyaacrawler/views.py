# Create your views here.
from django.shortcuts import render
from nyaacrawler.models import Anime,Torrent

from django.utils import simplejson

def index(request):
	anime = Anime.objects.all()
	torrent = Torrent.objects.all()

	context = {'animeList': anime, "torrentList":torrent}
	return render(request, 'index.html', context)
