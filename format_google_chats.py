import sys
import json
import base64
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 
from urllib import request
import chardet

# chardet.detect()

original_message_path = "messages.json"

file_name = 'sample_output.pdf'
document_title = 'sample'
title = 'Technology'
subtitle = 'MESSAGES BELOW'

def load_file(path):
    '''
    objective:
        load json file
    input:
        path - path of json file
    output:
        data - dictionary of messages
    '''

    # sys.version_info()
    f = open(path, encoding="utf-8")
    
    # returns JSON object as a dictionary
    data = json.load(f)
    
    # closing file
    f.close()
    
    return data



print("START TEST")

file_data_raw = load_file(original_message_path)

file_data = file_data_raw.get("messages", [])

pdf = canvas.Canvas(file_name) 
pdf.setTitle(document_title) 
pdf.setFillColorRGB(0, 0, 255) 
pdf.setFont("Courier-Bold", 24) 
pdf.drawCentredString(290, 720, subtitle)
pdf.line(30, 710, 550, 710)

initial_text_spacing = 700

def text_handler(message: dict) -> int:
    text_handler = pdf.beginText(40, initial_text_spacing)
    text_handler.setFont("Courier", 10)
    text_handler.setFillColor(colors.black)
    author_name = message["creator"]["name"]
    author_mail = message["creator"]["email"]
    text = message["text"]
    formatted_text = f"{author_name} - {author_mail} : {text}"
    text_handler.textLine(formatted_text)
    pdf.drawText(text_handler)
    return text_handler.getY()

def get_y_img_placement() -> int:
    print(f"initial_text_spacing : {initial_text_spacing}")
    new_y = 800 - initial_text_spacing 
    print(f"New Y : {new_y}")
    return new_y


def img_handler(message: dict) -> int:
    image_url = message["annotations"][0]["url_metadata"]["image_url"]
    text_handler = pdf.beginText(40, initial_text_spacing)
    text_handler.setFont("Courier", 10)
    text_handler.setFillColor(colors.black)
    author_name = message["creator"]["name"]
    author_mail = message["creator"]["email"]
    formatted_text = f"{author_name} - {author_mail} : (IMAGE)"
    text_handler.textLine(formatted_text)
    pdf.drawText(text_handler)
    print(f"image_url : {image_url} ")
    y_img_placement = get_y_img_placement()
    result = pdf.drawImage(image_url, 150, y_img_placement, height=200, preserveAspectRatio=True)
    print(f"img_handler : {result}")
    # return result
    return y_img_placement

    # pass
    

def unsupported_handler(message: dict):
    print(f"Cannot support the following message. Skipping : {message}")
    return 10

def get_message_type(message : dict) -> str:
    is_text = "text" in message
    if is_text:
        return "txt"
    is_image = "annotations" in message and "image_url" in message.get("annotations")[0]["url_metadata"]
    if is_image:
        return "img"
    is_file_upload = "attached_files" in message and "original_name" in message.get("attached_files")
    if is_file_upload:
        return "upl"
    return "no_handler_found"
    
def get_message_handler(type: str):
    message_handler_map = {
        "txt" : text_handler,
        "img" : img_handler
    }
    return message_handler_map.get(type, unsupported_handler)

for message in file_data:
    print(json.dumps(message, indent=2))

    message_type = get_message_type(message)

    print(f"message_type : {message_type}")
    
    message_handler = get_message_handler(type=message_type)

    placement_result = message_handler(message=message)

    print(f"placement_result : {placement_result}")

    print(f"initial_text_spacing 1: {initial_text_spacing}")


    if message_type != 'img':
        initial_text_spacing -= 10
    else:
        initial_text_spacing -= placement_result

    if initial_text_spacing < 100:
        pdf.showPage()
        initial_text_spacing = 800




try:
    pdf.save()
except Exception as e:
    print(f"Error Occurred : {e}")