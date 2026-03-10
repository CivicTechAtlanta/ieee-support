from handlers.base_message_handler import BaseMessageHandler
from reportlab.lib.colors import black
from handlers.pdf_handler import PDFHandler
from reportlab.pdfbase.pdfmetrics import stringWidth

import re
import logging

# Regex covering common emoji Unicode ranges
EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticons
    "\U0001F300-\U0001F5FF"  # Misc Symbols and Pictographs
    "\U0001F680-\U0001F6FF"  # Transport and Map
    "\U0001F1E0-\U0001F1FF"  # Flags
    "\U00002702-\U000027B0"  # Dingbats
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols
    "\U0001FA00-\U0001FA6F"  # Chess Symbols / Extended-A
    "\U0001FA70-\U0001FAFF"  # Symbols Extended-A
    "\U00002600-\U000026FF"  # Misc Symbols
    "\U0000FE00-\U0000FE0F"  # Variation Selectors
    "\U0000200D"             # Zero Width Joiner
    "\U00002764"             # Heart
    "]+",
    flags=re.UNICODE
)

def segment_text(text):
    """Split text into segments of (text, font_name) tuples."""
    segments = []
    last_end = 0
    for match in EMOJI_RE.finditer(text):
        if match.start() > last_end:
            segments.append((text[last_end:match.start()], "Courier"))
        segments.append((match.group(), "NotoEmoji"))
        last_end = match.end()
    if last_end < len(text):
        segments.append((text[last_end:], "Courier"))
    return segments

def mixed_string_width(text, font_size=10):
    """Calculate width of text that may contain emojis using appropriate fonts."""
    total = 0
    for segment_text_str, font_name in segment_text(text):
        total += stringWidth(segment_text_str, font_name, font_size)
    return total


class GoogleMessagesTextHandler(BaseMessageHandler):

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

    def process_message(self) -> None:
        author_name = self.message["creator"]["name"]
        author_mail = self.message["creator"]["email"]
        formatted_text = f"""({(self.transform_datetime(datetime_str=self.message["created_date"]))}) {author_name} - {author_mail} : {self.message["text"]}"""

        wrapped_lines = self.wrap_text(formatted_text, 520)

        for line in wrapped_lines:
            logging.info(f"wrapped_line : {line}")
            text_handler = self.pdf_handler.pdf.beginText(40, self.pdf_handler.pos_y)
            text_handler.setFillColor(black)
            for segment, font_name in segment_text(line):
                text_handler.setFont(font_name, 10)
                text_handler.textOut(segment)
            self.pdf_handler.pdf.drawText(text_handler)
            self.pdf_handler.pos_y -= self.gm_text_vertical_spacing
            self.handle_pagination()
        return True
