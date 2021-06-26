from view_base import ViewBase
from view_common import read_template_file

class SongView:
    def __init__(self, data_retriever):
        self._template = read_template_file('song_view.html')
        self._edit = read_template_file('edit_slides_button.html')
        self._data_retriever = data_retriever

    def render(self, song):
        return ViewBase().render(self._template\
            .replace("_SONG_NAME_", song['name'])\
            .replace("_LYRICS_", self._render_component(song, 'lyrics'))\
            .replace("_CHORDS_", self._render_component(song, 'chords'))\
            .replace("_LEAD_", self._render_component(song, 'lead'))\
            .replace("_SLIDES_", self._render_slides(song)))

    def _render_component(self, song, component):
        if component in song['file_ids']:
            href = "https://drive.google.com/file/d/" + song['file_ids'][component] + "/view?usp=sharing"
            return '<li> <a target="_blank" rel="noopener noreferrer" href="{}">[{}]</a></li>'.format(href, component)
        return ""

    def _render_slides(self, song):
        if 'slides' not in song['file_ids']:
            return "No slides present for this song"
        output = "<p>" + self._edit.replace('_SONG_NAME_', song['name']) + "</p>"
        slides = self._data_retriever.get_slide(song['name'])
        output = output + "<p>" + slides.replace('\n', '</br>').decode('utf-8') + "</p>"

        return output
