from nyaacrawler.models import Anime, Torrent, AnimeAlias
from nyaacrawler.utils import emailSender

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

def get_title_regex_string():
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

def get_meta_regex_string():
    
    rStr = ''
    # seeders
    rStr += '(\d+)\sseeder\(s\),\s'
    # leechers
    rStr += '(\d+)\sleecher\(s\),\s'
    # downloads (skipped)
    rStr += '\d+\sdownload\(s\)\s-\s'
    # size
    rStr += '(\d+(?:\.\d+)?\s[MG]iB)'
    
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
        'page' : 'rss',
        'cats' : ENGLISH_TRANSLATED,
        'filter' : TRUSTED_ONLY,
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
            'page' : 'rss',
            'cats' : ENGLISH_TRANSLATED, 
            'term' : anime_name,
            'offset' : offset
        }

        url = BASE_URL +'?'+ urllib.urlencode(query_parameters)
        num_rows = crawl_page(url, concurrent=True)

        continue_crawl = num_rows > 0
        offset += 1

def parse_row(title_regex, meta_regex, item):
    try:
        torrent_name = item.title.text
        url = item.guid.text
        torrent_link = item.link.text
        meta = item.description.text

        # extract data after some normalization
        res = title_regex.match(torrent_name.replace('_', ' '))
        meta_res = meta_regex.match(meta)

        if not res or not meta_res:
            return

        #get torrent info
        fansub = res.group(1)
        animeName = res.group(2)
        episode = res.group(3)
        quality = format(res.group(4))
        vidFormat = format(res.group(5))
        
        seeders = meta_res.group(1)
        leechers = meta_res.group(2)
        file_size = meta_res.group(3)

        #A new alias name is stored if it has not been detected yet
        
        anime_alias_obj, created = AnimeAlias.objects.get_or_create(
            title = animeName,
            defaults = {
                'anime' : Anime.get_unknown_placeholder()
            }
        )
        
        animeObj = anime_alias_obj.anime;

        if animeObj.official_title != Anime.UNKNOWN_ANIME:

            if (Torrent.objects.filter(url=url).exists()):
                print ("torrent already exist: " + torrent_name)
            else:
                info_hash = get_torrent_info_hash(torrent_link)
                torrentObj = Torrent.objects.create(
                        url           =   url,
                        torrent_name  =   torrent_name,
                        title         =   anime_alias_obj,
                        episode       =   episode,
                        fansub        =   fansub,
                        quality       =   quality,
                        vidFormat     =   vidFormat,
                        seeders       =   seeders,
                        leechers      =   leechers,
                        file_size     =   file_size,
                        infoHash      =   info_hash
                )
                
                print ("torrent for " + str(torrentObj) + ": " + torrent_name +" added")

                # torrent_arrived(torrentObj)

    except:
        print('Error at: ' + item.get_text())
        print('with error: ' + str(sys.exc_info()) + '\n')

def crawl_page(url, concurrent=False):
    """
    Scapes a specific nyaa.se page
    returns the number of rows
    """
    print ("Scraping page... " + url)

    title_regex = re.compile(get_title_regex_string())
    meta_regex = re.compile(get_meta_regex_string())

    c=urllib2.urlopen(url)

    soup=BeautifulSoup(c.read(), 'xml')

    record_list = soup.find_all('item')
    num_rows = len(record_list)

    if concurrent:
        import threading
        threads = [threading.Thread(target=parse_row, args=(title_regex, meta_regex, item)) for item in record_list]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

    else:
        for item in record_list:
            parse_row(title_regex, meta_regex, item)

    print 'Crawl completed'

    return num_rows
    
