#import threading, time, random
#from multiprocessing import Queue

from data_proxy import DataProxy
from data_common import cache_dir

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

class SongsDao(DataProxy):
    def __init__(self, sheets_client, drive_client):
        DataProxy.__init__(self, "sng")
        self._sheets_client = sheets_client
        self._drive_client = drive_client

    def get_song_names(self):
        names = sorted(self.get_all_keys())
        res = []
        for name in names:
            res.append(name.replace('_', ' '))
        return res

    def _get_remote_data(self, data_key):
        return self._get_remote_song(data_key)

    def _get_all_remote_data(self):
        sync = SongSync(self._get_remote_song)
        all_song_names = self._sheets_client.list_song_names()
        for song_name in all_song_names:
            sync.add(song_name)
        return sync.execute()

    def _set_remote_data(self, add_song_data):
        self._sheets_client.add_song(add_song_data['name'], '')
        song = {}
        song['name'] = add_song_data['name']
        song['file_ids'] = {}
        if 'slides' in add_song_data:
            song['slides'] = add_song_data['slides']
            #self._drive_client.update_slide_file(song)
        for component in all_song_components:
            if component in add_song_data:
                file_path = add_song_data[component]['path']
                file_name = file_path.split('/')[1]
                file_type = add_song_data[component]['type']

                if component == 'slides':
                    file_name = file_path.split('/')[1]
                song['file_ids'][component] = self._drive_client.add_song_component(component, file_path, file_name, file_type)
        self._add_remote_slides(song)
        return song

    def _update_remote_data(self, data, update_song_data):
        #self._sheets_client.update_song(data['name'], data['name'], '')
        song = {}
        song['name'] = update_song_data['name']
        song['file_ids'] = data['file_ids']
        self._drive_client.update_slide_file(song)
        for component in all_song_components:
            if 'slides' not in component and component in update_song_data:
                file_path = update_song_data[component]['path']
                file_name = file_path.split('/')[1]
                file_type = update_song_data[component]['type']

                if component == 'slides':
                    file_name = file_path.split('/')[1]
                file_id = None
                if component in song['file_ids']:
                    file_id = song['file_ids'][component]
                song['file_ids'][component] = self._drive_client.update_song_component(component, file_path, file_name, file_type, file_id)
        self._add_remote_slides(song)
        return song

    def _get_data_key(self, data):
        return data['name'].replace(' ', '_')

    def _get_remote_song(self, song_name):
        song = {}
        song['name'] = song_name
        song['file_ids'] = {}
        for component in all_song_components:
            res = self._drive_client.get_file_id(song_name, component)
            if res is not None:
                song['file_ids'][component] = res
        self._add_remote_slides(song)
        return song

    def _add_remote_slides(self, song):
        file = cache_dir + song['name'] + '.txt'
        if 'slides' in song['file_ids']:
            self._drive_client.download_slide(song['file_ids']['slides'], file)
            song['slides'] = open(file, 'r').read()
        else:
            song['slides'] = ''
