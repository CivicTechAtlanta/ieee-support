from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Register Noto Emoji font for emoji support
_font_path = os.path.join(os.path.dirname(__file__), '..', 'fonts', 'NotoEmoji-Regular.ttf')
pdfmetrics.registerFont(TTFont('NotoEmoji', _font_path))

class PDFHandler:
    def __init__(
        self,
        pdf_path : str,
        file_name : str,
        subtitle : str,
        init_y_position : int,
        maximum_y_position : int
    ) -> None:
        self.pdf_path = pdf_path
        self.init_y_position = init_y_position
        pdf = canvas.Canvas(file_name)
        pdf.setFillColorRGB(0, 0, 255)
        pdf.setFont("Courier-Bold", 24)
        pdf.drawCentredString(290, self.init_y_position, subtitle)
        pdf.line(30, self.init_y_position, 550, self.init_y_position)
        self.pos_y = ( init_y_position - 20)
        self.pdf = pdf
        self.maximum_y_position = maximum_y_position