#import threading, time, random
#from multiprocessing import Queue

from data_common import cache_dir
from database import db

all_song_components = ['lyrics', 'chords', 'lead', 'slides']

class SongSync:

    def __init__(self, get_remote_song):
        self._get_remote_song = get_remote_song
        #self._names = Queue()
        self._names = []
        self._songs = []
        #self._lock = threading.Lock()

    def add(self, song_name):
        #self._names.put(song_name)
        self._names.append(song_name)

    def execute(self):
        #threads = []
        #for i in range(1):
        #    thread = threading.Thread(target=self._task)
        #    threads.append(thread)
        #    thread.start()

        #for t in threads:
        #    t.join()
        #return self._songs
        for name in self._names:
            self._songs.append(self._get_remote_song(name))
        return self._songs

    #def _task(self):
    #    while not self._names.empty():
    #        name = self._names.get()
    #        song = self._get_remote_song(name)
    #        with self._lock:
    #            self._songs.append(song)

class SongsDao():
    def __init__(self, sheets_client, drive_client):
        self._sheets_client = sheets_client
        self._drive_client = drive_client

    def get(self, name):
        return db.get_song(name)

    def sync(self, force=False):
        if force:
            sync = SongSync(self._get_remote_song)
            all_song_names = self._sheets_client.list_song_names()
            for song_name in all_song_names:
                sync.add(song_name)
            songs = sync.execute()
            db.drop_songs()
            for song in songs:
                db.add_song(song)

    def get_all(self):
        return db.get_songs()

    def update(self, song_data):
        original = get(song_data['name'])
        if original is None:
            raise Exception("Cannot update song as it does not exist")
        song = {}
        song['file_ids'] = original['file_ids']
        song['name'] = original['name']
        self._merge_component(song, original, new, 'ccli', '')
        self._merge_component(song, original, new, 'notes', '')
        self._update_remote_data(song, song_data)
        db.update_song(song)
        return song

    def set(self, song_data):
        original = db.get_song(song_data['name'])
        if original:
            raise Exception("Cannot add song as it already exists")
        self._sheets_client.add_song(song_data['name'], '')
        song = {}
        song['name'] = song_data['name']
        song['file_ids'] = {}
        song['ccli'] = ''
        song['notes'] = ''
        for component in all_song_components:
            if component in song_data:
                file_path = song_data[component]['path']
                file_name = file_path.split('/')[1]
                file_type = add_song_data[component]['type']

                if component == 'slides':
                    file_name = file_path.split('/')[1]
                song['file_ids'][component] = self._drive_client.add_song_component(component, file_path, file_name, file_type)
        self._get_remote_slides(song)
        db.add_song(song)
        return song

    def get_song_names(self):
        return db.get_song_names()

    def _update_remote_data(self, song, song_data):
        for component in all_song_components:
            if component in song_data:
                file_path = song_data[component]['path']
                file_name = file_path.split('/')[1]
                file_type = song_data[component]['type']

                if 'slides' in component:
                    file_name = file_path.split('/')[1]
                file_id = None
                if component in song['file_ids']:
                    file_id = song['file_ids'][component]
                song['file_ids'][component] = self._drive_client.update_song_component(component, file_path, file_name, file_type, file_id)
        self._get_remote_slides(song)
        return song

    def _get_remote_song(self, song_name):
        song = {}
        song['name'] = song_name
        song['file_ids'] = {}
        for component in all_song_components:
            res = self._drive_client.get_file_id(song_name, component)
            if res is not None:
                song['file_ids'][component] = res
        self._get_remote_slides(song)
        return song

    def _get_remote_slides(self, song):
        file = cache_dir + song['name'] + '.txt'
        if 'slides' in song['file_ids']:
            self._drive_client.download_slide(song['file_ids']['slides'], file)
            song['slides'] = open(file, 'r').read()
        else:
            song['slides'] = ''

    def _merge_component(self, data, original, new, component, default):
        original_comp = original.get(component, default)
        data[component] = new.get(component, original_comp)
