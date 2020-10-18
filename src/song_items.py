from song_item import SongItem
import json

class SongItems:
    def __init__(self, file_name):
        songsstring = open(file_name, "r").read()
        all_songs = json.loads(songsstring)
        self._items = {}
        for item in all_songs['songList']:
            self._items[item['id']] = SongItem(item)

    def get_by_id(self, id):
        return self._items.get(id)
