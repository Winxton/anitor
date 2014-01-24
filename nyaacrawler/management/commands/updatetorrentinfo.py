from django.core.management.base import NoArgsCommand, make_option

from nyaacrawler.models import Anime,AnimeAlias,Torrent
import socket
import struct   
from random import randrange #to generate random transaction_id

import logging
logger = logging.getLogger(__name__)

class Command(NoArgsCommand):
    TRACKER = 'open.nyaatorrents.info'
    PORT = 6544

    help = 'updates seeds and leechers for active torrents'

    def handle_noargs(self, **options):
        active_torrents = Torrent.objects.exclude(title__anime=Anime.objects.get(official_title=Anime.UNKNOWN_ANIME))
        accumulator = []

        logger.info ("Updating Torrents ... ")

        for torrent in active_torrents:
            if (len(accumulator) < 50):
                accumulator.append(torrent)
            else:
                self.__update_seed_leech(accumulator)
                accumulator = []

        self.__update_seed_leech(accumulator)

        logger.info ( len(active_torrents) + " updated." )

    def __update_seed_leech(self, active_torrents):
        #Create the socket
        clisocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        clisocket.connect((self.TRACKER, self.PORT))

        #Protocol says to keep it that way
        connection_id=0x41727101980
        #We should get the same in response
        transaction_id = randrange(1,65535)

        packet=struct.pack(">QLL",connection_id, 0,transaction_id)
        clisocket.send(packet)
        res = clisocket.recv(16)
        action,transaction_id,connection_id=struct.unpack(">LLQ",res)

        packet_hashes = ""
        for torrent in active_torrents:
            packet_hashes = packet_hashes + torrent.infoHash.decode('hex')

        packet = struct.pack(">QLL", connection_id, 2, transaction_id) + packet_hashes

        clisocket.send(packet)
        res = clisocket.recv(8 + 12*len(active_torrents))

        index = 8
        for torrent in active_torrents:
            seeders, completed, leechers = struct.unpack(">LLL", res[index:index+12])
            torrent.seeders = seeders
            torrent.leechers = leechers

            if (seeders <= 5):
                logger.info ("Torrent: " + torrent.torrent_name + " deleted.")
                torrent.delete()
            else:
                torrent.save()

            index = index + 12
