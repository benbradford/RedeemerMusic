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
        self._sync_songs_from_files()
        self._sync_services_from_files()
        self._sync_slides_from_files()

    def _sync_songs_from_files(self):
        # sync from local
        local_songs = open(songs_file, "r").read()
        self._cache.songs = json.loads(local_songs)

    def _sync_services_from_files(self):
        local_services = open(services_file, 'r').read()
        self._cache.services = json.loads(local_services)

    def _sync_slides_from_files(self):
        self._cache.slides = []
        for song in self._cache.songs:
            slides = {}
            slides['name'] = song['name']
            file_name = cache_dir + song['name'] + '.txt'
            slides['slides'] = open(file_name, 'r').read()

            self._cache.slides.append(slides)

    def update_songs_files(self):
        print "updating songs"
        with open(songs_file, 'w') as f:
            json.dump(self._cache.songs, f)

    def update_services_files(self):
        print "updating services"
        with open(services_file, 'w') as f:
            json.dump(self._cache.services, f)

    def update_slides_files(self):
        print "updating slides"
        for slide in self._cache.slides:
            file_name = cache_dir + song + '.txt'
            f = open(file_name, "w")
            f.write(slide['slides'])
            f.close()
