from django.core.mail import send_mail
from django.conf import settings

from nyaacrawler.models import Anime, Torrent, Subscription
from anitor import settings

import logging
logger = logging.getLogger(__name__)

def send_registration_confirmation_email(registration_parameters):
    subject = "Anitor Subscription: " + registration_parameters['anime']
    body = "Hello! You have subscribed to " + registration_parameters['anime'] + " on " + settings.SITE_URL + ". \n\n"

    body += "You are currently subscribed to the following series: \n"
    for subscription in Subscription.get_subscriptions_for_email(registration_parameters['email']):
        body += subscription.anime.official_title + "\n"
    body += "\n"

    body += "To unsubscribe from the series: \"" + registration_parameters['anime'] + "\", visit the following URL:\n"
    body += settings.SITE_URL + "/unsubscribe/" + registration_parameters['unsubscribe_key']  + "/"

    logger.info ("Sending notification email to: " + registration_parameters['email'] + " for " + registration_parameters['anime'] )
    send_mail(subject,body, 'Anitor Notifier ' + '<'+settings.DEFAULT_FROM_EMAIL+'>', [registration_parameters['email']])

def send_notification_email(subscription_parameters):
    subject = "Episode " + str(subscription_parameters['episode'])  + " for " + subscription_parameters['anime'] +" has Arrived."
    body = "A new release of the Anime you have subscribed to has arrived.\n\n"
    body += str(subscription_parameters['anime']) + " was released by " + settings.SITE_URL + ".\n\n"
    body += "To download the torrent for " + subscription_parameters['anime'] + " - episode " + str(subscription_parameters['episode']) + ", go to the link:\n "
    body += str(subscription_parameters['torrent_url']) + "\n\n"
    body += "You received this email because this series is in your tracking list. "
    body += "To unsubscribe from the series: \"" + str(subscription_parameters['anime']) + "\", visit the following URL:\n"
    body += settings.SITE_URL + "/unsubscribe/" + str(subscription_parameters['unsubscribe_key']) + "/"

    logger.info ("Sending notification email to: " + subscription_parameters['email'] + " for " + subscription_parameters['anime'] + " episode " + subscription_parameters['episode'])
    send_mail(subject,body, 'Anitor Notifier' + '<'+settings.DEFAULT_FROM_EMAIL+'>', [subscription_parameters['email']])

