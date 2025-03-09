from django.conf import settings
from twilio.rest import Client
from database.getdata import *
import secrets

def send_sms(to, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body = message,
        from_= settings.TWILIO_NUMBER,
        to = to
    )

    return settings.TWILIO_NUMBER

def send_verification(user_id, to_number):
    otp = f"{secrets.randbelow(100000):05d}"
    message = f"Hello, your verification code is: {otp}"
    send_sms(to_number, message)
    insert_verification_number(user_id, otp)

def send_checkin(interval, destination, user_id): 
    from .queue import start_miss_scheduler
    message = "This is <app name>. Please check-in at <weburl>."
    send_sms(destination, message)
    start_miss_scheduler(interval, user_id)

def contact_emergency(user):
    to = user.emergency_contacts[0]     # emerg contact phone number
    minutes = user.sessions.check_ins_missed * user.sessions.check_in_freq # We can get the numbers missed * frequency to say how long we havn't heard from them
    message = f"Hello, {user.name} was supposed to check in with us {minutes} ago. Could you please check-in with them?"
    send_sms(to, message)
    