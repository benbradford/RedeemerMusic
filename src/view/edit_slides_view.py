from view_base import ViewBase
from view_common import read_template_file

class EditSlidesView:
    def __init__(self):
        self._template = read_template_file('edit_slides_view.html')

    def render(self, song, slides):
        print slides
        return ViewBase().render(self._template\
            .replace("_SONG_NAME_", song['name'])\
            .replace("_SLIDES_", slides))
