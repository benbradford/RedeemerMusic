from operator import itemgetter
import copy

class DataRetriever:
    def __init__(self, cache):
        self._cache = cache

    def get_song(self, song_name):
        for name, song in self._cache.songs.iteritems():
            if name == song_name:
                return copy.deepcopy(song)
        return None

    def get_song_names(self):
        song_names = []
        for name in self._cache.songs.keys():
            song_names.append(copy.deepcopy(name))
        return sorted(song_names)

    def get_slide(self, song_name):
        for key, service in self._cache.slides.iteritems():
            if service['name'] == song_name:
                return copy.deepcopy(s['slides'])
        return None

    def get_service(self, id):
        for key, service in self._cache.services.iteritems():
            if service['id'] == id:
                return copy.deepcopy(service)
        return None

    def get_services(self):
        services = []
        for key, service in self._cache.services.iteritems():
            services.append(copy.deepcopy(service))
        return services
