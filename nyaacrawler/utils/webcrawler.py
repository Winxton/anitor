from nyaacrawler.models import Anime, Torrent
from nyaacrawler.utils import emailSender

from bs4 import BeautifulSoup

import urllib2
import re

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

    #example: [fansub group] anime name - 05 [720p].mkv

    rStr = ''
    # fansub group
    rStr += '(?:\[(.+?)\])?'
    # title
    rStr += '\s(.+?)\s'
    # title/episode separator (assumes that everything is in English)
    rStr += '\-(?=[^A-Za-z]{2}).*?'
    # episode #
    rStr += '0?(\d+).*?'
    # quality
    rStr += '(?:.*?((?:\d+(?:p|P))|(?:\d+x\d+)).*?)?'
    # format
    rStr += '(?=(mkv|mp4|avi))'

    regex = re.compile(rStr)

    #url to crawl
    c=urllib2.urlopen('http://www.nyaa.se/?cats=1_37')

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
    			print "Item found: ", url
    			
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
    		#print('error deteccted')
    		#print(item.get_text())