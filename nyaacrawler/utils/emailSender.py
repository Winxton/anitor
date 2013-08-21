from django.core.mail import send_mail

from nyaacrawler.models import Anime, Torrent, Subscription
from anitor import settings

def send_registration_confirmation_email(anime):
    subject = "Anitor Subscription"
    body = "Hello! You have subscribed to " + anime
    """
    TODO: email message parameters
    """

def send_notification_email(email, message_parameters):
    subject = "Episode {0} of {1}".format(*message_parameters)+" has Arrived"
    body = "TODO"
    send_mail(subject,body,settings.DEFAULT_FROM_EMAIL, [email])
