import time
import random

def generate_thumbnail(image_id, size):
    time.sleep(1)
    return f"/thumbs/{image_id}_{size[0]}x{size[1]}.jpg"

def send_email(to, template):
    time.sleep(2)
    if random.random() < 0.7:
        raise Exception("SMTPConnectionError")
    return "email_sent"