from song_items import SongItems
from members import Members

import json
import sys, getopt

all_song_items = SongItems('res/songs.json')
all_members = Members('res/members.json')

def get_songs(service):
    songs = []
    for song in service['songs']:
        songs.append(all_song_items.get_by_id(song))
    return songs

def get_band(service):
    band = []
    for member in service['band']:
        band.append(all_members.get_by_id(member))
    return band

def get_service_from_args(improper_usage_message):
    argv = sys.argv[1:]
    service_file = None

    try:
        opts, args = getopt.getopt(argv, "s:f:t:",["service=","from=","to="])
    except getopt.GetoptError:
        raise Exception(improper_usage_message)
    for opt, arg in opts:
        if opt in ('-s', '--service'):
            service_file = arg
    if service_file == None:
        raise Exception("Missing service use -s to specify")

    return json.loads(open(service_file, "r").read())
