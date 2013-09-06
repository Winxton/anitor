from django import template
from urllib import urlencode

register = template.Library()

@register.filter
def magnet_link(torrent):
    params = {
        'dn'    :   torrent.torrent_name,
        'xt'    :   'urn:btih:%s' % torrent.infoHash,
    }        
    link = "magnet:?" + urlencode(params)
    return link