# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from nyaacrawler.models import Anime,Torrent,Subscription
from django.http import HttpResponse

import json

def index(request):
	anime = Anime.objects.all()
	torrent = Torrent.objects.all()

	context = {'animeList': anime, "torrentList":torrent}
	return render(request, 'index.html', context)

@require_http_methods(["POST"])
def save_subscription(request):
    results = {'success':False}
    """
    TODO: pass in subscription parameters,
    create parameter object
    """
    json_result = json.dumps(results)
    return HttpResponse(json_result, content_type='application/json')