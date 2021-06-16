from operator import itemgetter
import copy

def service_id_sorter(service):
    string_value = service['id']
    int_value = int(string_value)
    return int_value

class DataRetriever:
    def __init__(self, cache):
        self._cache = cache

    def get_songs(self):
        with self._cache.songs_lock():
            return copy.deepcopy(self._cache.get_songs())
            
    def get_song(self, song_name):
        with self._cache.songs_lock():
            if song_name in self._cache.get_songs():
                return copy.deepcopy(self._cache.get_songs()[song_name])
        return None

    def get_song_names(self):
        song_names = []
        with self._cache.songs_lock():
            for name in self._cache.get_songs().keys():
                song_names.append(copy.deepcopy(name))
        return sorted(song_names)

    def get_slide(self, song_name):
        with self._cache.slides_lock():
            if song_name in self._cache.get_slides():
                return self._cache.get_slides()[song_name]
        return None

    def get_service(self, id):
        with self._cache.services_lock():
            if id in self._cache.get_services():
                return copy.deepcopy(self._cache.get_services()[id])
        return None

    def get_services(self):
        services = []
        with self._cache.services_lock():
            for key, service in self._cache.get_services().iteritems():
                services.append(copy.deepcopy(service))

        return sorted(services, key=service_id_sorter)
