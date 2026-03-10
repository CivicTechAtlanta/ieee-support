from handlers.base_message_handler import BaseMessageHandler
from handlers.google_message_handler.gm_text_message_handler import GoogleMessagesTextHandler
from handlers.google_message_handler.gm_image_message_handler import GoogleMessagesImageHandler
from handlers.google_message_handler.gm_file_attachment_handler import GoogleMessagesFileAttachmentHandler
from handlers.unsupported_handler import UnsupportedHandler
from handlers.pdf_handler import PDFHandler
import json

import logging


def load_file(path : str) -> dict:
    '''
    objective:
        load json file
    input:
        path - path of json file
    output:
        data - dictionary of messages
    '''

    file_data = open(path, encoding="utf-8")
    
    # returns JSON object as a dictionary
    messages = json.load(file_data)
    
    # closing file
    file_data.close()
    
    return messages

def get_message_handler(pdf_handler : PDFHandler, message_source : str, message : dict[str, str]) -> BaseMessageHandler:
    '''
    objective:
        get message type
    input:
        message - dictionary of message
    output:
        type - type of message
    '''
    message_handler = UnsupportedHandler
    if message_source == "google_chats":
        message_handler = get_google_messages_message_type(message=message)
    return message_handler(pdf_handler=pdf_handler, message=message)

def get_google_messages_message_type(message : dict[str, str]) -> BaseMessageHandler:
    '''
    objective:
        get message type
    input:
        message - dictionary of message
    output:
        type - type of message
    '''
    is_text = "text" in message
    if is_text:
        return GoogleMessagesTextHandler
    is_image = "annotations" in message and "image_url" in message.get("annotations")[0]["url_metadata"]
    if is_image:
        return GoogleMessagesImageHandler
    is_file_upload = "attached_files" in message and "original_name" in message.get("attached_files")[0]
    if is_file_upload:
        return GoogleMessagesFileAttachmentHandler
    return UnsupportedHandler

def process_messages(pdf_handler : PDFHandler, messages : dict[str, str], message_source : str) -> None:
    '''
    objective:
        process messages
    input:
        messages - dictionary of messages
    output:
        None
    '''

    num_messages = len(messages)
    messages_processed = 0
    messages_failed = 0
    failure_reasons = []

    logging.info(f"Number of messages : {num_messages}")

    for message in messages:
        success = False
        message_index = messages_processed + 1
        logging.info(f"Processing message {message_index} of {num_messages}")
        logging.debug(json.dumps(message, indent=2))
        message_handler = get_message_handler(pdf_handler=pdf_handler, message_source=message_source, message=message)

        try:
            success = message_handler.process_message()
        except Exception as e:
            success = False
            message_handler.error_reason = str(e)

        if not success:
            messages_failed += 1
            reason = message_handler.error_reason or "Unknown error"
            failure_reasons.append(f"Message {message_index}: {reason}")
        messages_processed += 1

    logging.info(f"Total Messages Failed: {messages_failed}")
    for reason in failure_reasons:
        logging.info(f"  - {reason}")
    logging.info(f"Total Messages Succeeded: {messages_processed - messages_failed}")
    logging.info(f"Total Messages Processed: {messages_processed}")