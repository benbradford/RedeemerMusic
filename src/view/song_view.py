from view_base import ViewBase

class SongView:
    def __init__(self, drive_service, slides_helper):
        self._template = open('../res/display_song.html', "r").read()
        self._drive_service = drive_service
        self._slides_helper = slides_helper

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
            return '<li> <a href="{}">[{}]</a> </li>'.format(href, component)
        return ""

    def _render_slides(self, song):
        if 'slides' not in song['file_ids']:
            return "No slides present for this song"
        output = ""
        slides_file = '../bin/' + song['name'] + ".txt"
        self._drive_service.download_slide(song['file_ids']['slides'], slides_file)
        slides = self._slides_helper.paginate_lyrics(slides_file)
        for slide in slides:
            output = output + "<p>" + slide.replace('\n', '</br>').decode('utf-8') + "</p>"
        return output
