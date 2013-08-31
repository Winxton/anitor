from urllib import urlencode
import urllib2
import json

MAL_API_URL = "http://mal-api.com/anime/"
SEARCH_CALL = "search"

def get_anime_search_info(anime_name):
	"""
	Uses the MAL search API: http://mal-api.com/docs/#read_search_anime
	"""
	data = {'q' : anime_name}
	url = MAL_API_URL + SEARCH_CALL + "?" + urlencode(data)
	content = urllib2.urlopen(url).read()
	return content

def parse_image_url(url):
	parsed_url = url[:-5] + url[-4:]
	return parsed_url

def get_anime_image_url(anime_name):
	content_json = json.loads(get_anime_search_info(anime_name))
	
	if content_json:
		#usually the most accurate result
		firstResult = content_json[0]
		print parse_image_url(firstResult['image_url'])
	else:
		return None
