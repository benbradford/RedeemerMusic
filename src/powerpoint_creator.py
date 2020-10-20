from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import json

class PowerpointCreator:
    def __init__(self, songs, date):
        self._date = date

    def create(self):

        prs = Presentation()
        prs.slide_width = Inches(14)

        ppt_file = open('res/ppt/O_Great_God.json', "r").read()
        ppt_json = json.loads(ppt_file)

        blank_slide_layout = prs.slide_layouts[6]

        num_slides = len(ppt_json['slides'])

        for i in range(num_slides):
            lyrics = ppt_json['slides'][i]
            num_lines = lyrics.count('\n') + 1
            slide = prs.slides.add_slide(blank_slide_layout)
            fill = slide.background.fill
            fill.solid()
            fill.fore_color.rgb = RGBColor(0, 0, 0)

            width = height = Inches(1)
            left = Inches(6.5)
            top = Inches(self._get_top_margin_in_inches(num_lines))
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame

            p = tf.add_paragraph()
            p.text = lyrics
            p.font.size = Pt(40)
            p.font.color.rgb = RGBColor(255, 255, 255)
            p.alignment = PP_ALIGN.CENTER

            if i == num_slides-1:
                self._add_footer(slide, ppt_json['footer'])

        outfile = "bin/{}.ppt".format(self._date)
        prs.save(outfile)
        return outfile

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
