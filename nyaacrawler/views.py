# Create your views here.
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from nyaacrawler.models import *
from django.http import HttpResponse, HttpResponseRedirect
from nyaacrawler.utils.emailSender import send_registration_confirmation_email

import json

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
    
    response = []
    for torrent in torrent_list:
        torrentObj = {}
        torrentObj['fansub'] = torrent.fansub
        torrentObj['quality'] = torrent.quality
        torrentObj['torrent_link'] = torrent.url
        torrentObj['seeders'] = torrent.seeders
        torrentObj['leechers'] = torrent.leechers
        torrentObj['file_size'] = torrent.file_size
        response.append(torrentObj)

    return HttpResponse(json.dumps(response), content_type='application/json')

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
            
            user, created = User.objects.get_or_create(**user_form.cleaned_data)

            anime = Anime.objects.get(pk=subscription_request['anime_key'])

            #send subscription confirmation email
            if created:
                send_registration_confirmation_email(anime, user)

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

def confirm_email(request, subscription_activation_key):
    """
    Confirmation that the email belongs to a valid user (i.e not spam)
    """
    try:
        user = User.objects.get(subscription_activation_key=subscription_activation_key)
        user.set_confirmed_email()
        user.save()
        
        #update the current episode for subscription
        subscriptions = user.get_subscriptions()
        for subscription in subscriptions:
            subscription.current_episode = subscription.anime.current_episode()
            subscription.save()
        
        #TODO: template for unsubscribe, show current subscriptions
        return HttpResponse("Email has been confirmed")

    except Subscription.DoesNotExist: 
        return HttpResponseRedirect('/')

def unsubscribe(request, unsubscribe_key):
    try:
        subscription = Subscription.objects.get(unsubscribe_key=unsubscribe_key)
        subscription.delete()
        
        #TODO: template for unsubscribe
        return HttpResponse("Unsubscribed")

    except Subscription.DoesNotExist:
        return HttpResponseRedirect('/')
    
