import json

cache_dir = '../bin/cache/'

songs_file = cache_dir + 'songs.json'
services_file = cache_dir + 'services.json'
slides_file = cache_dir + 'slides.json'

class RemoteCacheManager:
    def __init__(self, cache, drive, sheets, slides_helper, local_cache_manager):
        self._cache = cache
        self._drive = drive
        self._sheets = sheets
        self._slides_helper = slides_helper
        self._song_components = ['lyrics', 'chords', 'lead', 'slides']
        self._local_cache_manager = local_cache_manager

    def sync(self):
        self.sync_songs()
        self.sync_services()
        self.sync_slides()

    def sync_songs(self):
        print "getting song names"
        song_names = self._sheets.list_song_names()
        self._cache.songs = []
        for name in song_names:
            print "syncing song " + name
            song = {}
            song['name'] = name
            song['file_ids'] = {}
            for component in self._song_components:
                file_id = self._drive.get_file_id(name, component)
                if file_id is not None:
                    song['file_ids'][component] = file_id
                    print "got file id for " + component
            self._cache.songs.append(song)
        self._local_cache_manager.update_songs_files()

    def sync_services(self):
        self._cache.services = self._sheets.get_services()
        self._local_cache_manager.update_services_files()

    def sync_slides(self):
        self._cache.slides = []
        for song in self._cache.songs:
            file = cache_dir + song['name'] + '.txt'
            if 'slides' in song['file_ids']:
                self._drive.download_slide(song['file_ids']['slides'], file)
                slides_from_song = self._slides_helper.paginate_lyrics(file)
            else:
                print "[WARN] No slides available for " + song['name']
                slides_from_song = "missing"
            slide = {}
            slide['name'] = song['name']
            slide['slides'] = slides_from_song
            self._cache.slides.append(slide)
