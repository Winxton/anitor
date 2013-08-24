# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from nyaacrawler.models import Anime,Torrent,Subscription,User
from django.http import HttpResponse, HttpResponseRedirect

import json

def index(request):
	anime = Anime.objects.all().exclude(official_title=Anime.UNKNOWN_ANIME)

	context = {'animeList': anime}
	return render(request, 'index.html', context)

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

@require_http_methods(["POST"])
def subscribe(request):
    """
    Saves a subscription given the email and a
    comma delimited list of fansub groups and qualities 
    """
    results = {'success':False}

    subscription_request = json.loads(request.body)

    subscription_new = Subscription.create(
        subscription_request['email'],
        subscription_request['key'],
        subscription_request['qualities'],
        subscription_request['fansub_groups']
    )
    print subscription_new
    print subscription_new.user

    json_result = json.dumps(results)
    return HttpResponse(json_result, content_type='application/json')

def unsubscribe(request, unsubscribe_key):
    try:
        subscription = Subscription.objects.get(unsubscribe_key=unsubscribe_key)
        subscription.delete()
        
        user = subscription.user
        if user.has_no_subscriptions():
            user.delete()
        
        #TODO: template for unsubscribe
        return HttpResponse("Unsubscribed")

    except Subscription.DoesNotExist:
        return HttpResponseRedirect('/')
    