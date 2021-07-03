#import threading, time, random
#from multiprocessing import Queue

from data_common import cache_dir
from db_access import DbAccess

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
        return self._db_get_song(name)

    def sync(self, force=False):
        if force:
            sync = SongSync(self._get_remote_song)
            all_song_names = self._sheets_client.list_song_names()
            for song_name in all_song_names:
                sync.add(song_name)
            songs = sync.execute()
            with DbAccess() as cur:
                cur.execute("delete from service")
            for song in songs:
                self._db_add_song(song)

    def get_all(self):
        songs = self._db_get_songs()
        res = {}
        for song in songs:
            res[song['name']] = song
        return res

    def update(self, song_name, file_uploads):
        song = self.get(song_name)
        if song is None:
            raise Exception("Cannot update song as it does not exist")
        for component in all_song_components:
            if component in file_uploads:
                file_path = file_uploads[component]['path']
                file_name = file_path.split('/')[1]
                file_type = file_uploads[component]['type']

                if 'slides' in component:
                    file_name = file_path.split('/')[1]
                file_id = None
                if component in song['file_ids']:
                    file_id = song['file_ids'][component]
                song['file_ids'][component] = self._drive_client.update_song_component(component, file_path, file_name, file_type, file_id)
        self._get_remote_slides(song)
        self._db_update_song(song)
        return song

    def set(self, song_data):
        original = self._db_get_song(song_data['name'])
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
        self._db_add_song(song)
        return song

    def get_song_names(self):
        return self._db_get_song_names()

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

    def _db_get_song(self, name):
        res = None
        with DbAccess() as cur:
            res = cur.execute('SELECT * FROM song where name=:song_name', {'song_name': name}).fetchall()
        if not res:
            return None
        return self._db_to_song(res[0])

    def _db_get_songs(self):
        songs = None
        with DbAccess() as cur:
            songs = cur.execute('SELECT * FROM song ORDER BY name').fetchall()
        res = []
        for song in songs:
            r = self._db_to_song(song)
            res.append(r)
        return res

    def _db_get_song_names(self):
        songs = None
        with DbAccess() as cur:
            songs = cur.execute('SELECT name FROM song ORDER BY name').fetchall()
        res = []
        for song in songs:
            res.append(song[0])
        return res

    def _db_add_song(self, song):
        return self.add_songs([song])

    def _db_add_songs(self, songs):
        with DbAccess() as cur:
            for song in songs:
                cur.execute("delete from song where name =:song_name", {'song_name': song['name']}).fetchall()
                cur.execute("""
                insert into song(name, ccli, notes, lyrics_id, chords_id, lead_id, slides_id, slides)
                values(?, ?, ?, ?, ?, ?, ?, ?);
                """, (song['name'],\
                            song.get('ccli', ''),\
                            song.get('notes', ''),\
                            song['file_ids'].get('lyrics', None),\
                            song['file_ids'].get('chords', None),\
                            song['file_ids'].get('lead', None),\
                            song['file_ids'].get('slides', None),\
                            song.get('slides', '')))

    def _db_update_song(self, song):
        with DbAccess() as cur:
            cur.execute("""
                update song set(ccli, notes, lyrics_id, chords_id, lead_id, slides_id, slides)=(?, ?, ?, ?, ?, ?, ?)
                where(name = ?)
                """,(song.get('ccli', ''),\
                song.get('notes', ''),\
                song['file_ids'].get('lyrics', None),\
                song['file_ids'].get('chords', None),\
                song['file_ids'].get('lead', None),\
                song['file_ids'].get('slides', None),\
                song.get('slides', ''),\
                song.get('name')))

    def _db_to_song(self, song):
        r = {}
        r['name'] = song[0]
        r['ccli'] = song[1]
        r['notes'] = song[2]
        r['file_ids'] = {}
        r['file_ids']['lyrics'] = song[3]
        r['file_ids']['chords'] = song[4]
        r['file_ids']['lead'] = song[5]
        r['file_ids']['slides'] = song[6]
        r['slides'] = song[7]
        return r
