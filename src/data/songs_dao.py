from data_common import cache_dir
from db_accessor import DbAccessor

all_song_components = ['lyrics', 'chords', 'lead', 'slides']


class SongsDao(DbAccessor):
    def __init__(self, sheets_client, drive_client):
        DbAccessor.__init__(self)
        self._sheets_client = sheets_client
        self._drive_client = drive_client

    def get(self, name):
        return self._db_get_song(name)

    def sync(self, force=False):
        if force:
            all_song_names = self._sheets_client.list_song_names()
            songs = []
            for name in all_song_names:
                songs.append(self._get_remote_song(name))
            with self.db_access() as cur:
                cur.execute("delete from song")
            for song in songs:
                self._db_add_songs([song])

    def get_song_names(self):
        with self.db_access() as cur:
            songs = cur.execute('SELECT name FROM song ORDER BY name').fetchall()
        res = []
        for song in songs:
            res.append(song[0])
        return res

    def get_all(self):
        songs = self._db_get_songs()
        res = {}
        for song in songs:
            res[song['name']] = song
        return res

    def update(self, song_name, song_creation_data):
        song = self.get(song_name)
        if song is None:
            raise Exception("Cannot update song as it does not exist")
        for component in all_song_components:
            if component in song_creation_data:
                path, name, type = SongsDao._get_path_name_type_from_creation_data(song_creation_data, component)
                file_id = None  # move to data param
                if component in song['file_ids']:
                    file_id = song['file_ids'][component]
                song['file_ids'][component] = self._drive_client.update_song_component(component, path, name, type,
                                                                                       file_id)
        self._add_remote_slides_to_song(song)
        self._db_update_song(song)
        return song

    def set(self, song, song_creation_data):
        original = self._db_get_song(song['name'])
        if original:
            raise Exception("Cannot add song as it already exists")

        self._sheets_client.add_song(song['name'], '')

        for component in all_song_components:
            if component in song_creation_data:
                path, name, type = SongsDao._get_path_name_type_from_creation_data(song_creation_data, component)
                song['file_ids'][component] = self._drive_client.add_song_component(component, path, name, type)
        self._add_remote_slides_to_song(song)
        self._db_add_songs([song])
        return song

    def _get_remote_song(self, song_name):
        song = {'name': song_name, 'file_ids': {}}
        for component in all_song_components:
            res = self._drive_client.get_file_id(song_name, component)
            if res is not None:
                song['file_ids'][component] = res
        self._add_remote_slides_to_song(song)
        return song

    def _add_remote_slides_to_song(self, song):
        file = cache_dir + song['name'] + '.txt'
        if 'slides' in song['file_ids'] and song['file_ids']['slides']:
            self._drive_client.download_slide(song['file_ids']['slides'], file)
            song['slides'] = open(file, 'r').read()
        else:
            song['slides'] = ''

    def _db_update_song(self, song):
        with self.db_access() as cur:
            cur.execute("""
                update song set(ccli, notes, lyrics_id, chords_id, lead_id, slides_id, slides)=(?, ?, ?, ?, ?, ?, ?)
                where(name = ?)
                """, (song.get('ccli', ''), song.get('notes', ''), song['file_ids'].get('lyrics', None),
                      song['file_ids'].get('chords', None), song['file_ids'].get('lead', None),
                      song['file_ids'].get('slides', None), song.get('slides', ''), song.get('name')))

    def _db_get_songs(self):
        with self.db_access() as cur:
            songs = cur.execute('SELECT * FROM song ORDER BY name').fetchall()
        res = []
        for song in songs:
            r = SongsDao._db_to_song(song)
            res.append(r)
        return res

    def _db_get_song(self, name):
        with self.db_access() as cur:
            res = cur.execute('SELECT * FROM song where name=:song_name', {'song_name': name}).fetchall()
        if not res:
            return None
        return SongsDao._db_to_song(res[0])

    def _db_add_songs(self, songs):
        with self.db_access() as cur:
            for song in songs:
                cur.execute("delete from song where name =:song_name", {'song_name': song['name']}).fetchall()
                cur.execute("""
                insert into song(name, ccli, notes, lyrics_id, chords_id, lead_id, slides_id, slides)
                values(?, ?, ?, ?, ?, ?, ?, ?);
                """, (song['name'],
                      song.get('ccli', ''),
                      song.get('notes', ''),
                      song['file_ids'].get('lyrics', None),
                      song['file_ids'].get('chords', None),
                      song['file_ids'].get('lead', None),
                      song['file_ids'].get('slides', None),
                      song.get('slides', '')))

    @staticmethod
    def _get_path_name_type_from_creation_data(song_creation_data, component):
        return song_creation_data[component]['file_path'], \
               song_creation_data[component]['file_name'], \
               song_creation_data[component]['file_type']

    @staticmethod
    def _merge_component(data, original, new, component, default):
        original_comp = original.get(component, default)
        data[component] = new.get(component, original_comp)

    @staticmethod
    def _db_to_song(song):
        r = {'name': song[0],
             'ccli': song[1],
             'notes': song[2],
             'file_ids': {'lyrics': song[3], 'chords': song[4], 'lead': song[5], 'slides': song[6]},
             'slides': song[7]}
        return r