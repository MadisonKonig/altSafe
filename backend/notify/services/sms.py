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

# TODO: We need to get the emergency contact of the user. 
# then, we want to send a text to them saying that checkins were missed.
def contact_emergency(user_id):
    user = None # user obj from mongoDB
    to = ""     # emerg contact phone number
    minutes = "" # We can get the numbers missed * frequency to say how long we havn't heard from them
    message = f"Hello, {user.name} was supposed to check in with us {minutes} ago. Could you please check-in with them?"
    send_sms(to, message)
    