
from drive_service import DriveService

folder_ids = {
    'lyrics': '1A0u-Fixg4uEjipe8ZL7rWoPg7E86cS5b',
    'chords': '13G13PpGFPeSmMI6YEjXiBwi7VYVYQMm8',
    'lead': '1PnliQdA9zmuu2s0n9PAzFbzz1JfLb6Hv',
    'slides': '10_hTK6keFv1gWx-OkFuImuDtqFU8PVRN'
}

components = ['lyrics', 'chords', 'lead', 'slides']

class SongsRetriever:

    def __init__(self):
        self._drive_service = DriveService()

    def get_song(self, name):
        song = {}
        song['name'] = name
        song['file_ids'] = {}
        for component in components:
            try:
                id = self._drive_service.get_file_id(song, component)
                song['file_ids'][component] = id
            except:
                print("[WARN] Cannot find " + component + " for " + song['name'])
        return song

    def get_song_names(self):
        items = self._drive_service.list_files(folder_ids['lyrics'])
        song_names = []
        for item in items:
            song_names.append(item['name'].replace(' (lyrics)', ''))
        return song_names
