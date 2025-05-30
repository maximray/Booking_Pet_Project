from email.message import EmailMessage

from pydantic import EmailStr

from app.config import Setting


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Booking confirmation"
    email["From"] = Setting.SMTP_USER
    email["To"] = email_to
    
    email.set_content(
        f"""
            <h1>Confirm your booking</h1>
            You booked hotel from {booking["date_from"]}  to {booking["date_to"]}
         """,
        subtype="html"
    )
    return email 
    