"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.test import TestCase

from nyaacrawler.models import Anime,Torrent, Subscription

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
            'key'   : 2,
            'qualities' : "720p,480p",
            'fansub_groups' : "somesubgroup",
            'episode'   : 10
        }
        resp = self.client.post('/subscribe/', content_type='application/json', data=json.dumps(subscription))
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual (json.loads(resp.content)['success'], False)

    def testSubscribeSuccess(self):

        subscription = {
            'email' : "test@example.com",
            'key'   : 2,
            'qualities' : "720p,480p",
            'fansub_groups' : "somesubgroup",
            'episode'   : 10
        }
        resp = self.client.post('/subscribe/', content_type='application/json', data=json.dumps(subscription))
        
        self.assertEqual(resp.status_code, 200)
        self.assertEqual (json.loads(resp.content)['success'], True)