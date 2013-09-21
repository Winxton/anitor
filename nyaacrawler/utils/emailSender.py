from django.core.mail import send_mail
from django.conf import settings

from nyaacrawler.models import Anime, Torrent, Subscription
from anitor import settings

def send_registration_confirmation_email(user, anime):
    subject = "Anitor Subscription Confirmation"
    body = "Hello! You have subscribed to " + unicode(anime) + "\n"
    body += "You received this email because this is your first subscription on " + settings.SITE_URL + ".\n"
    body += "Please go to " + settings.SITE_URL + "/" + " to confirm your subscription. "
    
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
