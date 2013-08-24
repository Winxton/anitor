from nyaacrawler.models import Anime, Torrent, AnimeAlias
#from nyaacrawler.utils import emailSender

from bs4 import BeautifulSoup

import urllib2
import re
import sys

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
        #subscription.save()

def crawl_anime():
    """
    an incremental crawl of torrents from nyaa.se
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
    result = soup.find_all('tr', {"class" : "tlistrow"})
    
    unidentifiedNames = []
    
    for item in result:
        try:
            nametd = item.find('td',{"class":'tlistname'})

            name = nametd.get_text()
            url = nametd.a['href']
            torrent_link = item.find('td',{"class":'tlistdownload'}).a['href']
            size = item.find('td',{'class':'tlistsize'}).get_text()
            seeders = item.find('td',{'class':'tlistln'}).get_text()
            leechers = item.find('td',{'class':'tlistdn'}).get_text()
            
            # extract data after some normalization
            res = regex.match(item.get_text().replace('_', ' '))
            
            if not res:
                continue
            
            fansub = res.group(1)
            animeName = res.group(2)
            episode = res.group(3)
            quality = format(res.group(4))
            vidFormat = format(res.group(5))

            animeObj = AnimeAlias.objects.filter(alias_name=animeName)
            
            if animeObj.count():
                animeObj = animeObj[0].anime;
                
                if str(animeObj) == "placeholder":
                    continue

                torrentObj, created = Torrent.objects.get_or_create(
                    url = url,
                    defaults = {
                        'anime'     :   animeObj,
                        'episode'   :   episode,
                        'fansub'    :   fansub,
                        'quality'   :   quality,       
                        'vidFormat' :   vidFormat,
                    }
                )
                
                # torrent_arrived(torrentObj)

            elif animeName not in unidentifiedNames:
                unidentifiedNames.append(animeName)

        except:
            print('Error at: ' + item.get_text())
            print('with error: ' + str(sys.exc_info()) + '\n')
    
    print ('Crawl completed')
    if len(unidentifiedNames):
        for name in sorted(unidentifiedNames):
            # store these names as alias to anime "placeholder"
            AnimeAlias.objects.get_or_create(
                anime = Anime.objects.get(title='placeholder'),
                alias_name = name
            )
        print ('new anime alias added')
