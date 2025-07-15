from handlers.pdf_handler import PDFHandler
from tasks import process_messages
from tasks import load_file
import logging
import sys

logging.basicConfig(level=logging.INFO)  # Set to DEBUG for more verbose logging

### FILE CONFIGURATION ###

pdf_path = "sample_messages/messages_more_pages.json"
file_name = "sample_output.pdf"
subtitle = "CIVIC TECH ATLANTA"

message_source = "google_chats"

initial_y_position = 800
maximum_y_position = 100

logging.debug("Inital variables set. Logs below are from the main function.")

if __name__ == "__main__":

    file_data_raw = load_file(path=pdf_path)
    messages = file_data_raw.get("messages", [])

    pdf_handler = PDFHandler(
        pdf_path=pdf_path,
        file_name=file_name,
        subtitle=subtitle,
        init_y_position=initial_y_position,
        maximum_y_position=maximum_y_position)

    try:
        process_messages(
            messages=messages,
            message_source=message_source,
            pdf_handler=pdf_handler)
    except Exception as e:
        logging.error(f"Error Occurred : {e}")
    finally:
        pdf_handler.pdf.save()
        logging.info(f"PDF saved successfully with name : {file_name}")
        sys.exit(0)