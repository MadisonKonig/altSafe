from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()
scheduler.start()


def schedule_checkin(interval, destination, user_id, callback):        
    scheduler.add_job(
        callback, 
        "interval", 
        minutes=interval, 
        args=[user_id, destination], 
        id=user_id,
        replace_existing=True  # Ensure it replaces any previous job with the same ID
        )


def schedluer_miss(interval, user_id, callback):
    run_time = datetime.now() + timedelta(minutes=interval)
    scheduler.add_job(
        callback, 
        "date", 
        run_time=run_time,
        args=[user_id], 
        id=f"{user_id}-miss", 
        replace_existing=True  # Ensure it replaces any previous job with the same ID
    )
