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
        self._slides = {} # name: slides
        self._songsLock = CacheLock()
        self._slidesLock = CacheLock()

    def update_songs(self, songs):
        with self._songsLock:
            self._songs = songs

    def update_slides(self, slides):
        with self._slidesLock:
            self._slides = slides

    def add_or_update_slide(self, name, slide):
        with self._slidesLock:
            self._slides[name] = slide

    def add_or_update_song(self, name, song):
        with self._songsLock:
            self._song[name] = song

    def songs_lock(self):
        return self._songsLock

    def slides_lock(self):
        return self._slidesLock

    def get_songs(self):
        return self._songs

    def get_slides(self):
        return self._slides
