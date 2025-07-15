from handlers.base_message_handler import BaseMessageHandler
from handlers.pdf_handler import PDFHandler
import logging

class UnsupportedHandler(BaseMessageHandler):
    def __init__(self, pdf_handler : PDFHandler, message : dict[str, str]) -> None:
        pass
        
    def process_message(self) -> bool:
        logging.info("This message has an unsupported type. Cannot output the current message.")
        return False
