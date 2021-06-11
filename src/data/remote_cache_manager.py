import json

cache_dir = '../bin/cache/'

songs_file = cache_dir + 'songs.json'
services_file = cache_dir + 'services.json'
slides_file = cache_dir + 'slides.json'

class RemoteCacheManager:
    def __init__(self, drive, sheets, local_cache_manager):
        self._drive = drive
        self._sheets = sheets
        self._song_components = ['lyrics', 'chords', 'lead', 'slides']
        self._local_cache_manager = local_cache_manager

    def sync(self):
        songs = self.sync_songs()
        self.sync_services()
        self.sync_slides(songs)
        self._local_cache_manager.sync()

    def sync_songs(self):
        print "getting song names"
        song_names = self._sheets.list_song_names()
        songs = {}
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
            songs[name] = song
        self._local_cache_manager.save_to_songs(songs)
        return songs

    def sync_services(self):
        services = {}
        services_arr = self._sheets.get_services()
        for service in services_arr:
            services[service['id']] = service
        self._local_cache_manager.save_to_services(services)

    def sync_slides(self, songs):
        for name, song in songs.iteritems():
            file = cache_dir + name + '.txt'
            if 'slides' in song['file_ids']:
                # TODO tell local cache manager to lock slide and download directly
                with self._local_cache_manager.slide_lock(name):
                    self._drive.download_slide(song['file_ids']['slides'], file)
            else:
                print "[WARN] No slides available for " + name
                slides_from_song = "missing"
