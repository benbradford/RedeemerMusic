import json

cache_dir = '../bin/cache/'

songs_file = cache_dir + 'songs.json'
services_file = cache_dir + 'services.json'
slides_file = cache_dir + 'slides.json'

class LocalCacheManager:
    def __init__(self, cache):
        self._cache = cache
        pass

    def sync(self):
        self._sync_songs()
        self._sync_services()
        self._sync_slides()

    def _sync_songs(self):
        # sync from local
        local_songs = open(songs_file, "r").read()
        self._cache.songs = json.loads(local_songs)

    def _sync_services(self):
        local_services = open(services_file, 'r').read()
        self._cache.services = json.loads(local_services)

    def _sync_slides(self):
        self._cache.slides = {}
        for name, song in self._cache.songs.iteritems():
            slides = {}
            slides['name'] = name
            file_name = cache_dir + name + '.txt'
            slides['slides'] = open(file_name, 'r').read()
            self._cache.slides['name'] = slides
