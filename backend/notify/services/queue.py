from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
import uuid

from .sms import send_checkin
from django.conf import settings

scheduler = BackgroundScheduler()

def start_notify_scheduler(interval, destination=None, user_id=None):
    if user_id is None:          # This is a use case only valid while mongoDB is not setup
        user_id = str(uuid.uuid4())
    if destination is None:
        destination = settings.DEFAULT_NUMBER
        
    scheduler.add_job(send_checkin, "interval", minutes=interval, args=[destination], id=user_id )
    if not scheduler.running: 
        scheduler.start()
        
    return user_id

def start_miss_scheduler(interval_setting, destination=None, user_id=None):
    if user_id is None:          # This is a use case only valid while mongoDB is not setup
        user_id = str(uuid.uuid4())
    if destination is None:
        destination = settings.DEFAULT_NUMBER
    
    current_time = datetime.now()
    trigger_time = current_time + timedelta(seconds=20)
    scheduler.add_job(
        add_missed, 
        DateTrigger(run_date=trigger_time), 
        args=[user_id, current_time], 
        id=f"{user_id}-check", 
        replace_existing=True  # Ensure it replaces any previous job with the same ID
    )

# This function needs to be in the db app.
# get the user, then check their latest check-in. if the check-in time after min_datetime, the user has not checked in
# If they haven't checked in, we need to increment the # of missed check-ins for the user session.
# THEN, if the missed check-ins exceed the threshold, we need to send the emergency contact a text message.
def add_missed(user_id, min_datetime):
    return
    
def stop_session(session_id):
    try:
        scheduler.remove_job(session_id)
        return True
    except JobLookupError:
        return False
    