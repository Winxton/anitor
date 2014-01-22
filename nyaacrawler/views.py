# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from nyaacrawler.utils.emailSender import send_registration_confirmation_email
from nyaacrawler.models import *
from urllib import urlencode

import sys

import json

import logging
logger = logging.getLogger(__name__)

def index(request):
    anime = Anime.get_active_anime()
    
    context = {'animeList': anime}
    return render(request, 'index.html', context)

def get_torrents_for_anime_episode(request):
    anime_id = request.GET.get('id')
    episode = request.GET.get('episode')
    
    torrent_list = Torrent.objects.filter(
        episode=episode,
        title__anime__pk=anime_id
    ).order_by('fansub')
    
    anime_title = Anime.objects.get(pk=anime_id).official_title;

    response = []
    for torrent in torrent_list:
        torrentObj = {}
        torrentObj['fansub'] = torrent.fansub
        torrentObj['quality'] = torrent.quality
        torrentObj['torrent_link'] = torrent.url
        
        params = {
            'dn'    :   anime_title,
            'xt'    :   'urn:btih:%s' % torrent.infoHash,
        }

        torrentObj['magnet_link'] = "magnet:?" + urlencode(params);
        torrentObj['seeders'] = torrent.seeders
        torrentObj['leechers'] = torrent.leechers
        torrentObj['file_size'] = torrent.file_size
        response.append(torrentObj)

    return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
@require_http_methods(["POST"])
def subscribe(request):
    """
    Saves a subscription given the email and a
    comma delimited list of fansub groups and qualities 
    """
    results = {'success':False}
    subscription_request = json.loads(request.body)
    
    try:
        anime = Anime.objects.get(pk=subscription_request['anime_key'])

        already_subscribed = Subscription.objects.filter(email=subscription_request['email'], anime=subscription_request['anime_key']).exists()

        if already_subscribed:
            results['error_message'] = "You have already subscribed to this anime."

        else:
            subscription_data = {
                'email' : subscription_request['email'],
                'anime' : subscription_request['anime_key'],
                'current_episode' : anime.current_episode(),
                'qualities' : subscription_request['qualities'],
                'fansubs' : subscription_request['fansub_groups'] 
            }

            subscription_form = SubscriptionForm(subscription_data)
            
            if (subscription_form.is_valid()):
                subscription, created = Subscription.objects.get_or_create(**subscription_form.cleaned_data)

                #send subscription confirmation email
                if created:
                    registration_parameters = {}
                    registration_parameters['email'] = subscription.email
                    registration_parameters['unsubscribe_key'] = subscription.unsubscribe_key
                    registration_parameters['anime'] = subscription.anime.official_title
                    
                    try:
                        send_registration_confirmation_email(registration_parameters)
                    except:
                        pass

                    results['success'] = True
                    logger.info ("Subscribed: " + subscription.email + " to " + subscription.anime.official_title)
            else:
                if 'email' in subscription_form.errors:
                    results['error_message'] = "Invalid email."
                elif 'fansubs' in subscription_form.errors:
                    results['error_message'] = "You must select a fansub."
                elif 'qualities' in subscription_form.errors:
                    results['error_message'] = "You must select a quality."

    except:
        logger.error ( str(sys.exc_info()) )

    json_result = json.dumps(results)
    return HttpResponse(json_result, content_type='application/json')

def unsubscribe(request, unsubscribe_key):
    try:
        subscription = Subscription.objects.get(unsubscribe_key=unsubscribe_key)
        
        response = "unsubscribed from " + subscription.anime.official_title
        logger.info ( subscription.email + " " + response )

        subscription.delete()
        
        #TODO: template for unsubscribe
        return HttpResponse( response )

    except Subscription.DoesNotExist:
        return HttpResponseRedirect('/')