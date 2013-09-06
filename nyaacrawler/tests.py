"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.test import TestCase

from nyaacrawler.models import *

import json

class NyaaView(TestCase):
    fixtures = ['nyaacrawler_testdata.json']

    def test_index(self):

        resp = self.client.get('/')
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('animeList' in resp.context)

    def testSubscribeBadEmail(self):

        subscription = {
            'email' : "bademail",
            'anime_key'   : 2,
            'qualities' : "720p,480p",
            'fansub_groups' : "somesubgroup",
            'episode'   : 10
        }
        resp = self.client.post('/subscribe/', content_type='application/json', data=json.dumps(subscription))
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual (json.loads(resp.content)['success'], False)

    def test_subscribe_confirm_unsubscribe(self):
        #subscribe
        subscription = {
            'email' : "test@example.com",
            'anime_key'   : 2,
            'qualities' : "720p,480p",
            'fansub_groups' : "somesubgroup",
            'episode'   : 10
        }
        resp = self.client.post('/subscribe/', content_type='application/json', data=json.dumps(subscription))
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual (json.loads(resp.content)['success'], True)

        #email confirmation
        user = User.objects.get(email="test@example.com")
        self.assertEqual (user.get_num_subscriptions(), 1)

        self.assertEqual (user.has_confirmed_email(), False)
        self.assertEqual (user.is_registered(), False)

        resp = self.client.get('/confirm-subscription/'+user.subscription_activation_key+'/')
        self.assertEqual (resp.status_code, 200)

        user = User.objects.get(email="test@example.com")
        self.assertEqual (user.has_confirmed_email(), True) #user is now activated

        #unsubscribe
        subscription = Subscription.objects.get(user__email="test@example.com")
        resp = self.client.get('/unsubscribe/'+subscription.unsubscribe_key+'/')
        
        self.assertEqual (resp.status_code, 200)
        self.assertEqual (user.get_num_subscriptions(), 0)
        self.assertEqual (Subscription.objects.filter(user__email="test@example.com").exists(), False)
