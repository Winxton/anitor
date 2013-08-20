from nyaacrawler.models import Anime, Torrent
from bs4 import BeautifulSoup
import urllib2
import re

def crawl_anime():
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

    for item in result:
        try:
            url = item.find("a")['href']
            
            # extract data after some normalization
            res = regex.match(item.get_text().replace('_', ' '))

            fansub = res.group(1)
            animeName = res.group(2)
            episode = res.group(3)
            quality = format(res.group(4))
            vidFormat = format(res.group(5))

            if Anime.objects.filter(title=animeName).count():
                animeObj = Anime.objects.get(title=animeName)

                #create if does not exist
                torrentObj, created = Torrent.objects.get_or_create(
                    anime = animeObj,
                    episode = episode,
                    fansub = fansub,
                    quality = quality,
                    url = url,						
                    vidFormat = vidFormat,
                )

        except:
            pass

    print ("k")