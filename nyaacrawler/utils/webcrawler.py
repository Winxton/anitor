from nyaacrawler.models import Anime, Torrent, AnimeAlias
#from nyaacrawler.utils import emailSender

from bs4 import BeautifulSoup

from hashlib import sha1
import bencode

import urllib
import urllib2
import re
import sys

#url parameters - subject to change
BASE_URL = 'http://www.nyaa.se/'
ENGLISH_TRANSLATED = '1_37'
TRUSTED_ONLY = 2

def torrent_arrived(torrent):
    """
    get all matching subscribers and send notification email
    """
    matched_subscriptions = torrent.get_matching_subscriptions()
    
    for subscription in matched_subscriptions:
        message_parameters = [torrent.episode, unicode(torrent.anime)]
        emailSender.send_notification_email (subscription.get_email(), message_parameters)
        subscription.increment_episode()
        #subscription.save()

def crawl_anime():
    """
    Scapes the front page of nyaa:
    an incremental crawl of torrents from nyaa.se which
    runs as a django-admin command
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
    query_parameters = {
        'cats' : ENGLISH_TRANSLATED,
        'filter' : TRUSTED_ONLY
    }

    url = BASE_URL + '?' + urllib.urlencode(query_parameters)

    print ("Scraping page... " + url)
    
    c=urllib2.urlopen(url)

    soup=BeautifulSoup(c.read())
    result = soup.find_all('tr', {"class" : "tlistrow"})
    
    unidentifiedNames = []
    
    for item in result:
        try:
            nametd = item.find('td',{"class":'tlistname'})

            torrent_name = nametd.get_text()
            
            # extract data after some normalization
            res = regex.match(torrent_name.replace('_', ' '))
            
            if not res:
                continue

            animeName = res.group(2)

            animeObj = AnimeAlias.objects.filter(alias_name=animeName)
            
            if animeObj.count():
                animeObj = animeObj[0].anime;
                
                if animeObj.official_title == "unknown-anime-placeholder":
                    continue

                #get torrent info
                fansub = res.group(1)
                episode = res.group(3)
                quality = format(res.group(4))
                vidFormat = format(res.group(5))

                url = nametd.a['href']
                torrent_link = item.find('td',{"class":'tlistdownload'}).a['href']
                size = item.find('td',{'class':'tlistsize'}).get_text()
                seeders = item.find('td',{'class':'tlistln'}).get_text()
                leechers = item.find('td',{'class':'tlistdn'}).get_text()

                info_hash = get_torrent_info_hash(torrent_link)
                
                torrentObj, created = Torrent.objects.get_or_create(
                    url = url,
                    defaults = {
                        'torrent_name'  : torrent_name,
                        'anime'     :   animeObj,
                        'episode'   :   episode,
                        'fansub'    :   fansub,
                        'quality'   :   quality,       
                        'vidFormat' :   vidFormat,
                        'infoHash'  :   info_hash
                    }
                )
                print ("torrent for " + str(torrentObj) + " added")
                # torrent_arrived(torrentObj)

            elif animeName not in unidentifiedNames:
                unidentifiedNames.append(animeName)

        except:
            print('Error at: ' + item.get_text())
            print('with error: ' + str(sys.exc_info()) + '\n')
            
    print ('Crawl completed')
    if len(unidentifiedNames):
        for name in sorted(unidentifiedNames):
            # store these names as alias to anime "unknown-anime-placeholder"
            AnimeAlias.objects.get_or_create(
                anime = Anime.objects.get(official_title='unknown-anime-placeholder'),
                alias_name = name
            )
        print ('new anime alias added')

def get_torrent_info_hash(torrent_link):
    rawdata = urllib2.urlopen(torrent_link).read();

    metainfo = bencode.bdecode(rawdata)

    obj = sha1(bencode.bencode(metainfo['info']) )

    return obj.hexdigest()