from view_base import ViewBase
from view_common import read_template_file

class SongsView:
    def __init__(self):
        self._template = read_template_file('songs_view.html')

    def render(self, song_names):
        return ViewBase().render(self._template.replace("_SONGS_", self._display_options(song_names)))

    def _display_options(self, song_names):
        output = ""
        for name in song_names:
            output += self._display_option(name, name.replace(" ", "%20"))
        return output

    def _display_option(self, name, id):
        return '<option value="' + id + '">' + name + '</option>'
