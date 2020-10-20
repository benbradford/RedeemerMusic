from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import json

class PowerpointCreator:
    def __init__(self, songs, out_file):
        self._out_file = out_file
        self._songs = songs

    def create(self):
        prs = self._create_empty_presentation()

        for song in self._songs:
            self._add_song(prs,song)
            self._add_blank_page(prs)

        outfile = "bin/{}".format(self._out_file)
        prs.save(outfile)
        return outfile

    def _create_empty_presentation(self):
        prs = Presentation()
        prs.slide_width = Inches(14)
        blank_slide_layout = prs.slide_layouts[6]
        return prs

    def _add_song(self, prs, song):
        pages = self._convert_lyrics_to_pages(song.get_ppt_file())
        num_pages = len(pages)

        for i in range(num_pages):
            lyrics = pages[i]
            num_lines = lyrics.count('\n') + 1
            slide = self._create_slide(prs)
            paragraph = self._create_paragraph(slide, num_lines)
            self._add_lyrics_to_paragraph(paragraph, lyrics)
            if i == num_pages-1:
                self._add_footer(slide, 'CCLI Licence No. 640402')

    def _add_blank_page(self, prs):
        self._create_slide(prs)

    def _convert_lyrics_to_pages(self, song_file):
        pages = []
        file = open(song_file, "r")
        lyrics = file.readline()

        # loop until EOF
        while lyrics != '':
            next = file.readline()
            while next != '\n' and next != '':
                # keep adding to lyrics until end of file or empty line
                lyrics = lyrics + next
                next = file.readline()

            # add accumulated lyrics to a single page
            if len(lyrics) > 1:
                pages.append(lyrics)

            # skip blank lines
            lyrics = file.readline()
            while lyrics == '\n':
                lyrics = file.readline()
                
        return pages

    def _create_slide(self, prs):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(0, 0, 0)
        return slide

    def _create_paragraph(self, slide, num_lines):
        width = height = Inches(1)
        left = Inches(6.5)
        top = Inches(self._get_top_margin_in_inches(num_lines))
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        return tf.add_paragraph()

    def _add_lyrics_to_paragraph(self, p, lyrics):
        p.text = lyrics
        p.font.size = Pt(40)
        p.font.color.rgb = RGBColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER

    def _get_top_margin_in_inches(self, num_lines):
        lines_to_inches = {
             1: 2.75,
             2: 2.5,
             3: 2.25,
             4: 2,
             5: 1.75,
             6: 1.5,
             7: 1.25,
             8: 0.7,
             9: 0.3
        }
        try:
            return lines_to_inches[num_lines]
        except:
            return 0

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
