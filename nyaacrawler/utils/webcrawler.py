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
    Gets all matching subscribers and send notification email
    """
    matched_subscriptions = torrent.get_matching_subscriptions()

    for subscription in matched_subscriptions:
        message_parameters = [torrent.episode, unicode(torrent.anime)]
        emailSender.send_notification_email (subscription.get_email(), message_parameters)
        subscription.increment_episode()
        #subscription.save()

def get_regex_string():
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

    return rStr

def get_torrent_info_hash(torrent_link):
    """
    Gets the info hash from a torrent file
    """
    rawdata = urllib2.urlopen(torrent_link).read();

    metainfo = bencode.bdecode(rawdata)

    obj = sha1(bencode.bencode(metainfo['info']) )

    return obj.hexdigest()

def crawl_anime():
    """
    Scapes the front page of nyaa:
    an incremental crawl of torrents from nyaa.se
    """
    #url to crawl
    query_parameters = {
        'cats' : ENGLISH_TRANSLATED,
        'filter' : TRUSTED_ONLY
    }

    url = BASE_URL + '?' + urllib.urlencode(query_parameters)
    crawl_page(url)

def crawl_specific_anime(anime_name):
    """
    Scrapes an anime using the search in nyaa.se
    """
    continue_crawl = True
    offset = 1

    while continue_crawl:

        query_parameters = {
            'page' : 'search',
            'cats' : ENGLISH_TRANSLATED, 
            'term' : anime_name,
            'offset' : offset
        }

        url = BASE_URL +'?'+ urllib.urlencode(query_parameters)
        num_rows = crawl_page(url)

        continue_crawl = num_rows > 0
        offset += 1

def crawl_page(url):
    """
    Scapes a specific nyaa.se page
    returns the number of rows
    """
    print ("Scraping page... " + url)

    regex = re.compile(get_regex_string())

    c=urllib2.urlopen(url)

    soup=BeautifulSoup(c.read())
    record_list = soup.find_all('tr', {"class" : "tlistrow"})

    num_rows = len(record_list)

    num_created = 0

    for item in record_list:
        try:
            nametd = item.find('td',{"class":'tlistname'})

            torrent_name = nametd.get_text()

            # extract data after some normalization
            res = regex.match(torrent_name.replace('_', ' '))

            if not res:
                continue

            #get torrent info
            fansub = res.group(1)
            animeName = res.group(2)
            episode = res.group(3)
            quality = format(res.group(4))
            vidFormat = format(res.group(5))

            url = nametd.a['href']
            torrent_link = item.find('td',{"class":'tlistdownload'}).a['href']
            size = item.find('td',{'class':'tlistsize'}).get_text()
            seeders = item.find('td',{'class':'tlistsn'}).get_text()
            leechers = item.find('td',{'class':'tlistln'}).get_text()

            unknown_placeholder = Anime.objects.get(official_title=Anime.UNKNOWN_ANIME)
            anime_alias_obj, created = AnimeAlias.objects.get_or_create(
                title = animeName,
                defaults = {
                    'anime' : unknown_placeholder
                }
            )

            animeObj = anime_alias_obj.anime;

            """
            If this anime title has been confirmed, calculate the info hash
            Calculating the info hash is an expensive process, so it is 
            only calculated if the alias is confirmed
            """

            torrentObj, created = Torrent.objects.get_or_create(
                url = url,
                defaults = {
                    'torrent_name'  :   torrent_name,
                    'title'         :   anime_alias_obj,
                    'episode'       :   episode,
                    'fansub'        :   fansub,
                    'quality'       :   quality,
                    'vidFormat'     :   vidFormat,
                    'seeders'       :   seeders,
                    'leechers'      :   leechers
                }
            )
            
            if animeObj.official_title != Anime.UNKNOWN_ANIME and not torrentObj.infoHash and anime_alias_obj.accepted:
                torrentObj.infoHash = get_torrent_info_hash(torrent_link)
                torrentObj.save()

            if created:
                print ("torrent for " + str(torrentObj) + ": " + torrent_name +" added")
                num_created += 1
                # torrent_arrived(torrentObj)
            else:
                print ("torrent already exist: " + torrent_name)
                # update data
            print ('')

        except:
            print('Error at: ' + item.get_text())
            print('with error: ' + str(sys.exc_info()) + '\n')

    print 'Crawl completed: ', num_created, " torrent(s) created."

    return num_rows