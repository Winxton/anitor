from django.core.mail import send_mail
from django.conf import settings

from nyaacrawler.models import Anime, Torrent, Subscription
from anitor import settings

def send_registration_confirmation_email(anime, user):
    subject = "Anitor Subscription"
    body = "Hello! You have subscribed to " + anime.official_title + ". "
    body += "Since this is your first subscription, please confirm your email here: "
    body += "http://<TBD>.<TBD>/confirm-subscription/"+user.subscription_activation_key
    
    """
    TODO: email message parameters
    """

def send_notification_email(subscription_parameters):
    subject = "Episode " + str(subscription_parameters['episode'])  + " for " + str(subscription_parameters['anime']) +" has Arrived."
    body = "A new release of the Anime you have subscribed to has arrived.\n\n"
    body += str(subscription_parameters['anime']) + " was released by " + settings.SITE_URL + ".\n\n"
    body += "To download the torrent for " + str(subscription_parameters['anime']) + " - episode " + str(subscription_parameters['episode']) + ", go to the link:\n "
    body += str(subscription_parameters['torrent_url']) + "\n\n"
    body += "You received this email because this series is in your tracking list. "
    body += "To unsubscribe from the series: \"" + str(subscription_parameters['anime'])+ "\", visit the following URL:\n"
    body += settings.SITE_URL + "/unsubscribe/" + str(subscription_parameters['unsubscribe_key']) + "/"

    send_mail(subject,body,settings.DEFAULT_FROM_EMAIL, [email])
