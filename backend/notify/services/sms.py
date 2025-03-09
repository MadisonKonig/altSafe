from django.conf import settings
from twilio.rest import Client
import secrets

def send_sms(to, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body = message,
        from_= settings.TWILIO_NUMBER,
        to = to
    )

    return settings.TWILIO_NUMBER

# TODO: update DB verify value with otp
def send_verification(to):
    otp = f"{secrets.randbelow(100000):05d}"
    message = f"Hello, your verification code is: {otp}"
    send_sms(to, message)

def send_checkin(to): 
    message = "This is <app name>. Please check-in at <weburl>."
    send_sms(to, message)