from handlers.base_message_handler import BaseMessageHandler
from handlers.pdf_handler import PDFHandler
from reportlab.lib.colors import black

import logging

class GoogleMessagesImageHandler(BaseMessageHandler):
    def __init__(self, pdf_handler : PDFHandler, message : dict[str, str]) -> None:
        super().__init__(pdf_handler=pdf_handler, message=message)
        

    def process_message(self) -> bool:
        image_url = self.message["annotations"][0]["url_metadata"]["image_url"]
        text_handler = self.pdf_handler.pdf.beginText(40, self.pdf_handler.pos_y)
        text_handler.setFont("Courier", 10)
        text_handler.setFillColor(black)
        author_name = self.message["creator"]["name"]
        author_mail = self.message["creator"]["email"]
        formatted_text = f"""({(self.transform_datetime(datetime_str=self.message["created_date"]))}) {author_name} - {author_mail} :(IMAGE BELOW)"""
        text_handler.textLine(formatted_text)
        self.pdf_handler.pdf.drawText(text_handler)
        logging.info(f"image_url : {image_url} ")
        self.pdf_handler.pos_y -= self.gm_text_vertical_spacing

        logging.info(f"CURRENT POS Y : {self.pdf_handler.pos_y}")
        image_y_pos = -(self.gm_image_height_limit - self.pdf_handler.pos_y)
        result = self.pdf_handler.pdf.drawImage(image_url, 150, image_y_pos, height=self.gm_image_height_limit, preserveAspectRatio=True)
        logging.info(f"result : {result}")
        self.pdf_handler.pos_y -= 220
        logging.info(f"POS Y After : {self.pdf_handler.pos_y}")
        self.handle_pagination()
        return True
