from handlers.base_message_handler import BaseMessageHandler
from reportlab.lib.colors import black, white
from handlers.pdf_handler import PDFHandler
from handlers.google_message_handler.gm_text_message_handler import segment_text, mixed_string_width

import os
import logging

IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp'}

class GoogleMessagesFileAttachmentHandler(BaseMessageHandler):

    def __init__(self, pdf_handler : PDFHandler, message : dict[str, str]) -> None:
        super().__init__(pdf_handler=pdf_handler, message=message)

    def wrap_text(self, text: str, max_width: int = 520) -> list[str]:
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if mixed_string_width(current_line + word) <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def draw_line(self, line: str) -> None:
        logging.info(f"wrapped_line : {line}")
        text_handler = self.pdf_handler.pdf.beginText(40, self.pdf_handler.pos_y)
        text_handler.setFillColor(black)
        for segment, font_name in segment_text(line):
            text_handler.setFont(font_name, 10)
            text_handler.textOut(segment)
        self.pdf_handler.pdf.drawText(text_handler)
        self.pdf_handler.pos_y -= self.gm_text_vertical_spacing
        self.handle_pagination()

    def find_file(self, attached_file: dict) -> str | None:
        """Try to find the attached file on disk, return absolute path or None."""
        json_dir = os.path.dirname(os.path.abspath(self.pdf_handler.pdf_path))
        candidates = [
            os.path.join(json_dir, attached_file.get("export_name", "")),
            os.path.join(json_dir, attached_file.get("original_name", "")),
        ]
        for path in candidates:
            if path and os.path.isfile(path):
                return path
        return None

    def draw_image(self, image_path: str) -> None:
        """Draw the image on the PDF."""
        image_y = self.pdf_handler.pos_y - self.gm_image_height_limit
        self.pdf_handler.pdf.drawImage(
            image_path, 150, image_y,
            width=self.gm_image_height_limit, height=self.gm_image_height_limit,
            preserveAspectRatio=True)
        self.pdf_handler.pos_y -= (self.gm_image_height_limit + 20)
        self.handle_pagination()

    def draw_image_not_found(self) -> None:
        """Draw a black box with 'Image not found.' text."""
        box_x = 150
        box_width = 200
        box_height = 40
        box_y = self.pdf_handler.pos_y - box_height

        self.pdf_handler.pdf.saveState()
        self.pdf_handler.pdf.setFillColor(black)
        self.pdf_handler.pdf.rect(box_x, box_y, box_width, box_height, fill=1, stroke=0)
        self.pdf_handler.pdf.setFillColor(white)
        self.pdf_handler.pdf.setFont("Courier", 10)
        self.pdf_handler.pdf.drawString(box_x + 10, box_y + 15, "Image not found.")
        self.pdf_handler.pdf.restoreState()

        self.pdf_handler.pos_y -= (box_height + 20)
        self.handle_pagination()

    def process_message(self) -> bool:
        author_name = self.message["creator"]["name"]
        author_mail = self.message["creator"]["email"]
        datetime_str = self.transform_datetime(datetime_str=self.message["created_date"])

        for attached_file in self.message["attached_files"]:
            file_name = attached_file.get("original_name", "Unknown file")
            formatted_text = f"({datetime_str}) {author_name} - {author_mail} : [FILE: {file_name}]"
            wrapped_lines = self.wrap_text(formatted_text, 520)
            for line in wrapped_lines:
                self.draw_line(line)

            _, ext = os.path.splitext(file_name)
            if ext.lower() in IMAGE_EXTENSIONS:
                file_path = self.find_file(attached_file)
                if file_path:
                    logging.info(f"Drawing attached image: {file_path}")
                    self.draw_image(file_path)
                else:
                    logging.info(f"Attached image not found: {file_name}")
                    self.draw_image_not_found()

        return True
