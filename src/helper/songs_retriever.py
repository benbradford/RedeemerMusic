
COMPONENTS = ['lyrics', 'chords', 'lead', 'slides']

class SongsRetriever:

    def __init__(self, drive_service):
        self._drive_service = drive_service

    def get_song(self, name, components = COMPONENTS):
        song = {}
        song['name'] = name
        song['file_ids'] = {}
        for component in components:
            try:
                id = self._drive_service.get_file_id(song['name'], component)
                song['file_ids'][component] = id
            except:
                print("[WARN] Cannot find " + component + " for " + song['name'])
        return song

    def get_song_names(self):
        items = self._drive_service.list_files('lyrics')
        song_names = []
        for item in items:
            song_names.append(item['name'].replace(' (lyrics)', ''))
        return song_names