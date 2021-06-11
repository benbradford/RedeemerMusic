import threading

class CacheLock:
    def __init__(self):
        self._lock = threading.Lock()

    def __enter__(self):
        self._lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock.release()


class Cache:
    def __init__(self):
        self._songs = {} # name: { name, file_ids {lyrics, chords, lead, slides} }
        self._services = {} # id: {id, date, extra, lead, band1, band2, band3, band4, song1, song2, song3, song4}
        self._slides = {} # name: slides
        self._songsLock = CacheLock()
        self._servicesLock = CacheLock()
        self._slidesLock = CacheLock()

    def update_songs(self, songs):
        with self._songsLock:
            self._songs = songs

    def update_services(self, services):
        with self._servicesLock:
            self._services = services

    def update_slides(self, slides):
        with self._slidesLock:
            self._slides = slides

    def add_slide(self, name, slide):
        with self._slides_Lock:
            self._slides[name] = slide

    def songs_lock(self):
        return self._songsLock

    def services_lock(self):
        return self._servicesLock

    def slides_lock(self):
        return self._slidesLock

    def get_songs(self):
        return self._songs

    def get_services(self):
        return self._services

    def get_slides(self):
        return self._slides
