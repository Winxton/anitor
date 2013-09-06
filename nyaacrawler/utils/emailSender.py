from django.core.mail import send_mail

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

def send_notification_email(email, message_parameters):
    subject = "Episode {0} of {1}".format(*message_parameters)+" has Arrived"
    body = "TODO"
    send_mail(subject,body,settings.DEFAULT_FROM_EMAIL, [email])
