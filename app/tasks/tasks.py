import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import Setting
from app.tasks.celery import celery
from app.tasks.email_templates import create_booking_confirmation_template


@celery.task
def process_pic(
    path: str,
):
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_1000_500 = im.resize((1000,500))
    im_resized_200_100 = im.resize((200,100))
    im_resized_1000_500.save(f"app/static/images/resized_1000_500_{im_path.name}")
    im_resized_200_100.save(f"app/static/images/resized_200_100_{im_path.name}")

@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    
    email_to = email_to
    msg_content = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(Setting.SMTP_HOST, Setting.SMTP_PORT) as server:
        server.login(Setting.SMTP_USER, Setting.SMTP_PASS)
        server.send_message(msg_content)
        