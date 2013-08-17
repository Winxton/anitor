from nyaacrawler.models import Anime, Torrent

import urllib2
import re
import sys

from bs4 import BeautifulSoup
from urlparse import urljoin

import difflib

def crawlAnime():
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
				"""
				print (torrentObj.anime.title, torrentObj.episode, torrentObj.fansub, torrentObj.quality, 								torrentObj.format, torrentObj.url)
               	"""
		except:
			pass
			e = sys.exc_info()
			print e

			#print('error deteccted')
			#print(item.get_text())

	for anime in uniqueAnime:
		print anime




