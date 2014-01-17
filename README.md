anitor
======

Anime Torrent organizer and aggregator: http://www.anitor.net

Gets seasonal anime list from [anichart](http://anichart.net) and categorizes torrents from [nyaa](http://nyaa.se).
Subscribed users will receive email updates when a new episode is available.

## Requirements

* Python v.2.x

* Django v.1.5 or v.1.6

* BeautifulSoup 4
http://www.crummy.com/software/BeautifulSoup/#Download

* lxml
http://www.crummy.com/software/BeautifulSoup/bs4/doc/#parser-installation

## Installation

1. Install the requirements above. The requirements are in requirements.txt, which can be installed with pip: `pip install -r requirements.txt`
2. Rename anitor/settings.py.sample and rename the file to settings.py. Sqlite3 is the default since it is easiest to configure, but mysql is used in production.
3. Initialize the database: `./manage.py syncdb`
4. Scrape current anime list: `./manage.py newseason`
5. Scrape the torrents for all animes `./manage.py initialize_aliases`
6. Run! `./manage.py runserver`

## Design

Each season, a list of Anime is added from anichart.net. Each anime title is inserted into both the *Anime* Model and the *AnimeAlias* Model. 

**Why have anime alias names?** <br />
*AnimeAlias* is needed since fansubs give different titles to each Anime.
For example, one fansub may give the japanese title, while the other gives the english title.

When an undetected title is scraped, it is added as an *AnimeAlias*, with *Anime* name "unknown-anime-placeholder". This can then be changed manually to the correct anime.

## Commands

`./manage.py newseason`

* Get the anime for the current season from http://anichart.net

`./manage.py initialize_aliases`

* Scrapes http://nyaa.se for the *AnimeAlias* names which have the do_initialize field set to true

`./manage.py incr_crawl`

* Scrapes http://nyaa.se up to the last date inside anitor/rss_fetch_datetime

`./manage.py updatetorrentinfo`

* Updates torrent info in the database (number of seeders and leechers) 

incr_crawl and updatetorrentinfo are run periodically via cron. A better alternative is to use a message queue.
