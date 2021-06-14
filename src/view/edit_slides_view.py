from view_base import ViewBase

class EditSlidesView:
    def __init__(self):
        self._template = open('../res/edit_slides_view.html', "r").read()

    def render(self, song, slides):
        return ViewBase().render(self._template\
            .replace("_SONG_NAME_", song['name'])\
            .replace("_SLIDES_", slides))
