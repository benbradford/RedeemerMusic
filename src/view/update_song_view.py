from view_base import ViewBase
from view_common import read_template_file

class UpdateSongView:
    def __init__(self, song_name, data_retriever):
        self._template = read_template_file('update_song_view.html')
        self._data_retriever = data_retriever
        self._song_name = song_name

    def render(self):
        song = self._data_retriever.get_song(self._song_name)
        return ViewBase().render(self._template) \
            .replace('_SONG_NAME_', song['name']) \
            .replace('_CCLI_', "") \
            .replace('_LYRICS_', self._replace_component(song, 'lyrics'))\
            .replace('_CHORDS_', self._replace_component(song, 'chords'))\
            .replace('_LEAD_', self._replace_component(song, 'lead'))

    def _replace_component(self, song, comp):
        if comp in song['file_ids']:
            href = "https://drive.google.com/file/d/" + song['file_ids'][comp] + "/view?usp=sharing"
            return '<a target="_blank" rel="noopener noreferrer" href="{}">[{}]</a>' .format(href, 'current')
        return ''
