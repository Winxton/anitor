"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.test import TestCase

from nyaacrawler.models import Anime,Torrent, Subscription

class nyaaView(TestCase):
    
    def test_index(self):

        anime_1 = Anime.objects.create(
            official_title = "evangelion"
        )

        anime_2 = Anime.objects.create(
            official_title = "Angel Beats"
        )
        
        resp = self.client.get('/')
        
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('animeList' in resp.context)
        
    def test_subscription(self):
        resp = self.client.post('/subscription/')
        self.assertEqual(resp.status_code, 200)
        