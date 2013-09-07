# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from nyaacrawler.models import *
from django.http import HttpResponse, HttpResponseRedirect

import json

def index(request):
    anime = Anime.get_active_anime()
    
    context = {'animeList': anime}
    return render(request, 'index.html', context)

def get_anime_list(request):
    search_string = request.GET.get('search')

    response = []
    
    anime_list = Anime.get_active_anime().filter(official_title__icontains=search_string)
    
    for anime in anime_list:
        animeObj = {}
        animeObj['pk'] = anime.pk
        animeObj['title'] = anime.official_title
        animeObj['torrents'] = []
        animeObj['image'] = anime.image
        

        torrent_list = anime.latest_episodes()
        for torrent in torrent_list:
            torrentObj = {}
            torrentObj['fansub'] = torrent.fansub
            torrentObj['quality'] = torrent.quality
            torrentObj['seeders'] = torrent.seeders
            torrentObj['leechers'] = torrent.leechers
            torrentObj['torrent_link'] = torrent.url
            torrentObj['file_size'] = torrent.file_size

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
    
    try:

        email_data = {
            'email' : subscription_request['email']
        }

        user_form = UserForm(email_data)
        
        if (user_form.is_valid()):

            user = user_form.save()
            anime = Anime.objects.get(pk=subscription_request['key'])

            subscription = Subscription(
                user = user,
                anime = anime,
                current_episode = subscription_request['episode'],
                qualities = subscription_request['qualities'],
                fansubs = subscription_request['fansub_groups'] 
                )
            
            subscription.full_clean()
            subscription.save()
            results['success'] = True

        else:
            results['errors'] = user_form.errors

    except ValidationError, e:
        results['errors'] = "Invalid subscription parameters"

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
    
