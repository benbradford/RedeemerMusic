import json

cache_dir = '../bin/cache/'

songs_file = cache_dir + 'songs.json'
services_file = cache_dir + 'services.json'
slides_file = cache_dir + 'slides.json'

class RemoteCacheManager:
    def __init__(self, drive, sheets, slides_helper, local_cache_manager):
        self._drive = drive
        self._sheets = sheets
        self._slides_helper = slides_helper
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
        with open(songs_file, 'w') as f:
            json.dump(songs, f, indent=4)
        return songs

    def sync_services(self):
        services = {}
        services_arr = self._sheets.get_services()
        for service in services_arr:
            services[service['id']] = service
        with open(services_file, 'w') as f:
            json.dump(services, f, indent=4)

    def sync_slides(self, songs):
        for name, song in songs.iteritems():
            file = cache_dir + name + '.txt'
            if 'slides' in song['file_ids']:
                self._drive.download_slide(song['file_ids']['slides'], file)
                slides_from_song = self._slides_helper.paginate_lyrics(file)
            else:
                print "[WARN] No slides available for " + name
                slides_from_song = "missing"

    def update_slides_files(self):
        print "updating slides"
        for slide in self._cache.slides:
            file_name = cache_dir + song + '.txt'
            f = open(file_name, "w")
            f.write(slide['slides'])
            f.close()
