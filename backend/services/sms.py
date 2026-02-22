from django.conf import settings
from twilio.rest import Client


def send_sms(to: str, message: str):
    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )

    client.messages.create(
        body=message,
        from_=settings.TWILIO_NUMBER,
        to=to
    )