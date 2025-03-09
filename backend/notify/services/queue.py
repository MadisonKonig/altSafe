from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
import uuid

from .sms import send_checkin
from django.conf import settings

scheduler = BackgroundScheduler()

def start_scheduler(interval, destination=None, session_id=None):
    if session_id is None:          # This is a use case only valid while mongoDB is not setup
        session_id = str(uuid.uuid4())
    if destination is None:
        destination = settings.DEFAULT_NUMBER
        
    scheduler.add_job(send_checkin, "interval", minutes=interval, args=[destination], id=session_id )
    if not scheduler.running: 
        scheduler.start()
        
    return session_id

def stop_session(session_id):
    try:
        scheduler.remove_job(session_id)
        return True
    except JobLookupError:
        return False
    