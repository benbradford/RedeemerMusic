import json
import threading
import copy
from data_common import cache_dir

class LocalFilesLock:
    def __init__(self):
        self._lock = threading.Lock()

    def __enter__(self):
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()


songs_file = cache_dir + 'songs.json'
services_file = cache_dir + 'services.json'
slides_file = cache_dir + 'slides.json'

class LocalCacheManager:
    def __init__(self, cache):
        self._cache = cache
        self._songFilesLock = LocalFilesLock()
        self._servicesFilesLock = LocalFilesLock()
        self._slidesFilesLock = {}
        self._masterSlidesLock = LocalFilesLock()

    def sync(self):
        self.sync_songs()
        self.sync_services()
        self.sync_slides()

    def save_to_songs(self, songs):
        with self._songFilesLock:
            with open(songs_file, 'w') as f:
                json.dump(songs, f, indent=4)

    def save_to_services(self, services):
        with self._servicesFilesLock:
            with open(services_file, 'w') as f:
                json.dump(services, f, indent=4)

    def with_slide_locked(self, name, func):
        with self._slide_lock(name):
            func()

    def sync_songs(self):
        local_songs = ""
        with self._songFilesLock:
            local_songs = open(songs_file, "r").read()
        self._cache.update_songs(json.loads(local_songs))

    def sync_services(self):
        local_services = ""
        with self._servicesFilesLock:
            local_services = open(services_file, 'r').read()
        self._cache.update_services(json.loads(local_services))

    def sync_slides(self):
        slides = {}
        with self._cache.songs_lock():
            for name, song in self._cache.get_songs().iteritems():
                file_name = cache_dir + name + '.txt'
                with self._slide_lock(name):
                    slides[name] = open(file_name, 'r').read().replace('\r', '')
        self._cache.update_slides(slides)

    def sync_slide(self, song):
        slides = ""
        with self._cache.songs_lock():
            file_name = cache_dir + song['name'] + '.txt'
            with self._slide_lock(song['name']):
                slides = open(file_name, 'r').read()
        self._cache.add_or_update_slide(song['name'], slides)

    def sync_song(self, song):
        with self._cache.songs_lock():
            songs = copy.deepcopy(self._cache.get_songs())
        songs[song['name']] = song
        self.save_to_songs(songs)
        self.sync_songs()

    def _slide_lock(self, name):
        with self._masterSlidesLock:
            if name not in self._slidesFilesLock:
                self._slidesFilesLock[name] = LocalFilesLock()

        return self._slidesFilesLock[name]

    def _append_lyrics_block(self, accumulated, file, paginated_lyrics):
        next = file.readline()
        while next != '\n' and next != '' and len(next) > 2:
            accumulated = accumulated + next
            next = file.readline()
        paginated_lyrics.append(accumulated.replace('\r', ''))

    def _skip_blank_lines(self, file):
        accumulated = file.readline()
        while accumulated == '\n' or accumulated == '\r' or accumulated == ' ':
            accumulated = file.readline()
        return accumulated
