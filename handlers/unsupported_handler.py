from handlers.base_message_handler import BaseMessageHandler
from handlers.pdf_handler import PDFHandler
import logging

class UnsupportedHandler(BaseMessageHandler):
    def __init__(self, pdf_handler : PDFHandler, message : dict[str, str]) -> None:
        self.message = message
        self.error_reason = None

    def process_message(self) -> bool:
        self.error_reason = "Unsupported message type"
        logging.info("This message has an unsupported type. Cannot output the current message.")
        return False
