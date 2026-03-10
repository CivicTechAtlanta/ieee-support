from abc import ABC
from handlers.pdf_handler import PDFHandler
from datetime import datetime

from typing import Final


class BaseMessageHandler(ABC):

    gm_text_vertical_spacing : Final[int] = 20
    gm_image_height_limit : Final[int] = 200

    def __init__(self, pdf_handler : PDFHandler, message : dict[str, str]) -> None:
        self.pdf_handler = pdf_handler
        self.message = message
        self.error_reason = None

    def handle_pagination(self) -> None:
        if self.pdf_handler.pos_y < self.pdf_handler.maximum_y_position:
            self.pdf_handler.pdf.showPage()
            self.pdf_handler.pos_y = self.pdf_handler.init_y_position

    def transform_datetime(self, datetime_str: str, dt_format : str = "%A, %B %d, %Y at %I:%M:%S %p %Z") -> str:
        """
        Transform a datetime string to a datetime object and then to an ISO 8601 string.

        The dt_format default value comes from google messages' datetime format. Other message sources may require a different format.

        The default is : "%A, %B %d, %Y at %I:%M:%S %p %Z"
        """
        dt = datetime.strptime(datetime_str, dt_format)
        return dt.isoformat()

    def process_message(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method")
    
