from nyaacrawler.models import Anime, Torrent
from nyaacrawler.utils import emailSender

import urllib2
import re
import sys

from bs4 import BeautifulSoup
from urlparse import urljoin

import difflib

def torrent_arrived(torrent):
    """
    get all matching subscribers and send notification email
    """
    torrent = Torrent.objects.filter(episode=19).get(pk=5)

    matched_subscriptions = torrent.get_matching_subscriptions()
    
    for subscription in matched_subscriptions:
        message_parameters = [torrent.episode, unicode(torrent.anime)]
        emailSender.send_notification_email (subscription.get_email(), message_parameters)
        subscription.increment_episode()
        subscription.save()

def crawl_anime():
    """
    an incremental crawl of torrents from nyaa.eu
    run as a django-admin command
    """

    #example: [subgroup] anime name - 05 [720p].mkv
    regex = re.compile('(?:\[(.+?)\])?\s?(.+?)\s?\-.*?0?(\d+)\s?.*?(?:.*?((?:\d+p)|(?:\d+x\d+)).*?)?(?:(?=(mkv|mp4|avi)))')

    #url to crawl
    c=urllib2.urlopen('http://www.nyaa.eu/?cats=1_37&term=shingeki+no+kyojin')

    soup=BeautifulSoup(c.read())
    result = soup.find_all('td', {"class" : "tlistname"})

    uniqueAnime = []

    for item in result:
    	#print (item.get_text())

    	try:
    		#extract torrent info
    		res = regex.match(item.get_text().replace('_', ' '))

    		fullStr = res.group(0)
    		fansub = res.group(1)
    		animeName = res.group(2)

    		#print('Anime: ' + animeName)
    		if animeName not in uniqueAnime:
    			uniqueAnime.append(animeName)

    		episode = res.group(3)
    		vidFormat = format(res.group(5))
    		quality = format(res.group(4))

    		#None handling
    		if fansub is None:
    			print ("????????? fansub")
    			fansub = "?"
    		if vidFormat is None:
    			print ("????????? vidformat")
    			vidFormat = "?"
    		if quality is None:
    			print ("????????? quality")
    			quality = "?"

    		num_results = Anime.objects.filter(title=animeName).count()

    		if num_results == 1:
    			#print "anime match"
    			animeObj = Anime.objects.get(title=animeName)

    			#print (animeObj.title)
    			url = item.find("a")['href']
    			print url
    			
                #create if does not exist
    			torrentObj, created = Torrent.objects.get_or_create(
    				anime = animeObj,
    				episode = episode,
    				fansub = fansub,
    				quality = quality,
    				url = url,						
    				vidFormat = vidFormat,
    			)

                torrent_arrived(torrentObj)
    	except:
    		pass
    		e = sys.exc_info()
    		print e

    		#print('error deteccted')
    		#print(item.get_text())