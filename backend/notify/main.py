from django.conf import settings
from twilio.rest import Client

def send_sms(to):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body = "This is <app name>. Please check-in at <weburl>.",
        from_= settings.TWILIO_NUMBER,
        to = "+17787100773"
    )

    return settings.TWILIO_NUMBER