from operator import itemgetter

class DataRetriever:
    def __init__(self, cache):
        self._cache = cache

    def get_song(self, song_name):
        for song in self._cache.songs:
            if song['name'] == song_name:
                return song
        return None

    def get_song_names(self):
        song_names = []
        for song in self._cache.songs:
            song_names.append(song['name'])
        return sorted(song_names)

    def get_slide(self, song_name):
        for s in self._cache.slides:
            if s['name'] == song_name:
                return s['slides']
        return None

    def get_service(self, id):
        for service in self._cache.services:
            if service['id'] == id:
                return service
        return None

    def get_services(self):
        return self._cache.services
