from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def send_sms(to: str, message: str):
    try:    
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )
        client.messages.create(
            body=message,
            from_=settings.TWILIO_NUMBER,
            to=to
        )
    except TwilioRestException as e:
        print(f"Error sending SMS: {e}")