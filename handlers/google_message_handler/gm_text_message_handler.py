from handlers.base_message_handler import BaseMessageHandler
from reportlab.lib.colors import black
from handlers.pdf_handler import PDFHandler
from reportlab.pdfbase.pdfmetrics import stringWidth

import logging

class GoogleMessagesTextHandler(BaseMessageHandler):

    def __init__(self, pdf_handler : PDFHandler, message : dict[str, str]) -> None:
        super().__init__(pdf_handler=pdf_handler, message=message)

    def wrap_text(self, text: str, max_width: int = 520) -> list[str]:
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if stringWidth(current_line + word, "Courier", 10) <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def process_message(self) -> None:
        author_name = self.message["creator"]["name"]
        author_mail = self.message["creator"]["email"]
        formatted_text = f"""({(self.transform_datetime(datetime_str=self.message["created_date"]))}) {author_name} - {author_mail} : {self.message["text"]}"""

        wrapped_lines = self.wrap_text(formatted_text, 520)

        for line in wrapped_lines:
            logging.info(f"wrapped_line : {line}")
            text_handler = self.pdf_handler.pdf.beginText(40, self.pdf_handler.pos_y)
            text_handler.setFont("Courier", 10)
            text_handler.setFillColor(black)
            text_handler.textLine(line)
            self.pdf_handler.pdf.drawText(text_handler)
            self.pdf_handler.pos_y -= self.gm_text_vertical_spacing
            self.handle_pagination()
        return True
