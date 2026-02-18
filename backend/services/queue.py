from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from database.getdata import *

from .sms import send_checkin, contact_emergency

scheduler = BackgroundScheduler()

def start_notify_scheduler(interval, destination, user_id):        
    scheduler.add_job(send_checkin, "interval", minutes=interval, args=[interval, destination, user_id], id=user_id )
    if not scheduler.running: 
        scheduler.start()
        
    return user_id

def start_miss_scheduler(interval_setting, user_id):
    current_time = datetime.now()
    trigger_time = current_time + timedelta(round(minutes=interval_setting / 4))
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
def add_missed(user_id, time_sent):
    user = get_data(user_id)
    sessions = user['sessions']
    if len(sessions):
        check_ins = sessions['check_ins']
        last_check_in = check_ins[-1]
        if last_check_in.timestamp < time_sent:
            updated_session = miss_check_in(user_id).sessions
            if (updated_session.check_in_threshold - updated_session.check_ins_missed < 1):
                contact_emergency(user)
    return
    
def stop_session(user_id):
    try:
        scheduler.remove_job(user_id)
        return True
    except JobLookupError:
        return JobLookupError
    
