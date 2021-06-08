from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import json

class SlidesHelper:
    def __init__(self, drive_service):
        self._drive_service = drive_service

    def create_powerpoint(self, service, out_file):
        song_files = self._download_song_files(service)
        presentation = self._create_empty_presentation()

        for song_file in song_files:
            self._add_slides_for_song(presentation, song_file)
            self._add_blank_page(presentation)

        presentation.save(out_file)
        return out_file

    def paginate_lyrics(self, song_file):
        # '\n' denotes a line seperator
        paginated_lyrics = []
        file = open(song_file, "r")

        next_line = file.readline()
        while next_line != '':
            self._append_lyrics_block(next_line, file, paginated_lyrics)
            next_line = self._skip_blank_lines(file)

        return paginated_lyrics

    def _download_song_files(self, service):
        song_files = []
        for index in [1,2,3,4,5, 6]:
            song_key = "song" + str(index)
            if song_key in service and service[song_key] != "":
                song_file = "../bin/" + service[song_key] + ".txt"
                file_id = self._drive_service.get_file_id(service[song_key], 'slides')
                self._drive_service.download_slide(file_id, song_file)
                song_files.append(song_file)
        return song_files

    def _create_empty_presentation(self):
        empty = Presentation()
        empty.slide_width = Inches(14)
        blank_slide_layout = empty.slide_layouts[6]
        return empty

    def _add_slides_for_song(self, presentation, song_file):
        paginated_lyrics = self._paginate_lyrics(song_file)
        num_slides_with_lyrics = len(paginated_lyrics)

        for i in range(num_slides_with_lyrics):
            self._assemble_page(paginated_lyrics[i], presentation, i == num_slides_with_lyrics-1, song_file)

    def _assemble_page(self, lyrics_on_page, presentation, is_last_slide, song):
        num_lines = lyrics_on_page.count('\n') + 1
        slide = self._create_slide(presentation)
        paragraph = self._create_paragraph(slide, num_lines, song)
        self._add_lyrics_to_paragraph(paragraph, lyrics_on_page)
        if is_last_slide:
            self._add_footer(slide, 'CCLI Licence No. 640402')

    def _add_blank_page(self, presentation):
        self._create_slide(presentation)

    def _append_lyrics_block(self, accumulated, file, paginated_lyrics):
        next = file.readline()
        while next != '\n' and next != '' and len(next) > 2:
            accumulated = accumulated + next
            next = file.readline()
        paginated_lyrics.append(accumulated.replace('\r', ''))

    def _skip_blank_lines(self, file):
        accumulated = file.readline()
        while accumulated == '\n' or accumulated == '\r' or accumulated == ' ':
            accumulated = file.readline()
        return accumulated

    def _create_slide(self, presentation):
        slide = presentation.slides.add_slide(presentation.slide_layouts[6])
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(0, 0, 0)
        return slide

    def _create_paragraph(self, slide, num_lines, song):
        width = height = Inches(1)
        left = Inches(6.5)
        top = Inches(self._get_top_margin_in_inches(num_lines, song))
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        return tf.add_paragraph()

    def _add_lyrics_to_paragraph(self, p, lyrics):
        p.text = lyrics
        p.font.size = Pt(54)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    def _get_top_margin_in_inches(self, num_lines, song):
        lines_to_inches = {
             1: 2.75,
             2: 2.5,
             3: 2.25,
             4: 2,
             5: 1.75,
             6: 1.5,
             7: 1.25,
             8: 0.7,
             9: 0.3,
             10: 0
        }
        try:
            return lines_to_inches[num_lines]
        except:
            raise Exception("Exceeded max allowed lines on a page {}/{} for {}".format(num_lines, 10, song))

    def _add_footer(self, slide, footer):
        width = height = Inches(1)
        left = Inches(13.0)
        top = Inches(6.9)
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        p = tf.add_paragraph()
        p.text = footer
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.RIGHT
