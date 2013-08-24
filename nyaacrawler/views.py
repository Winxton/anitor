# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from nyaacrawler.models import Anime,Torrent,Subscription
from django.http import HttpResponse

import json

def index(request):
	anime = Anime.objects.all().exclude(official_title=Anime.UNKNOWN_ANIME)

	context = {'animeList': anime}
	return render(request, 'index.html', context)

@require_http_methods(["POST"])
def save_subscription(request):
    """
    Saves a subscription
    given the email and a comma delimited list 
    of fansub groups and qualities 
    """
    results = {'success':False}
    
    json_result = json.dumps(results)
    return HttpResponse(json_result, content_type='application/json')

def get_anime_list(request):
    search_string = request.GET.get('search')

    response = []
    
    anime_list = Anime.objects.filter(official_title__icontains=search_string).exclude(official_title=Anime.UNKNOWN_ANIME)
    
    for anime in anime_list:
        animeObj = {}
        animeObj['pk'] = anime.pk
        animeObj['title'] = anime.official_title
        animeObj['torrents'] = []
        
        torrent_list = anime.latest_episodes()
        for torrent in torrent_list:
            torrentObj = {}
            torrentObj['fansub'] = torrent.fansub
            torrentObj['quality'] = torrent.quality
            animeObj['torrents'].append(torrentObj)

        response.append(animeObj)

    return HttpResponse(json.dumps(response), content_type='application/json')