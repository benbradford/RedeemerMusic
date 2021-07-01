from data_proxy import DataProxy
from data_common import cache_dir

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
        return self._get_song(data_key)

    def _get_all_remote_data(self):
        songs = []
        all_song_names = self._sheets_client.list_song_names()
        for song_name in all_song_names:
            songs.append(self._get_song(song_name))
        return songs

    def _set_remote_data(self, data):
        self._sheets_client.add_song(data['name'], '')
        self._drive_client.add_song(data) #TODO

    def _update_remote_data(self, data):
        self._sheets_client.update_song(data['name'], data['name'], '')
        self._drive_client.update_song2(data) #TODO

    def _get_data_key(self, data):
        return data['name'].replace(' ', '_')

    def _get_song(self, song_name):
        song = {}
        song['name'] = song_name
        song['file_ids'] = {}
        for component in ['lyrics', 'chords', 'lead', 'slides']:
            song['file_ids'][component] = self._drive_client.get_file_id(song_name, component)
        file = cache_dir + song_name + '.txt'
        if 'slides' in song['file_ids']:
            self._drive_client.download_slide(song['file_ids']['slides'], file)
            song['slides'] = open(file, 'r').read()
        else:
            song['slides'] = ''
        return song
