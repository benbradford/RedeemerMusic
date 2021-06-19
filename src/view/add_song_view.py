from view_base import ViewBase
from view_common import read_template_file

class AddSongView:
    def __init__(self):
        self._template = read_template_file('add_song_view.html')

    def render(self):
        return ViewBase().render(self._template)
