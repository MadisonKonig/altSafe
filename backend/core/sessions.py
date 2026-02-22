# core/sessions.py

from database.sessions import (
    start_session as start_session_db,
    end_session as end_session_db,
    add_check_in as add_check_in_db,
    increment_missed as increment_missed_db,
    get_active_session
)
from services.sms import send_sms


# ---------------------------
# SESSION LIFECYCLE
# ---------------------------

def start_user_session(user_id: str, threshold: int, freq: int, emergency_contact: str):
    """
    Start a new monitoring session.
    Enforces no overlapping sessions.
    """

    existing = get_active_session(user_id)

    if existing:
        raise Exception("Session already active")

    session_id = start_session_db(user_id, threshold, freq, emergency_contact)

    return {"status": "Session started successfully", "session_id": session_id}


def end_user_session(user_id: str):
    """
    End active session.
    """
    session = get_active_session(user_id)

    if not session:
        raise Exception("No active session")
    
    end_session_db(user_id, session["_id"])

    return {"status": "Session ended successfully"}


# ---------------------------
# CHECK-IN LOGIC
# ---------------------------

def add_check_in(user_id: str, location: str, notes: str | None):
    """
    Add a check-in and reset missed counter.
    """

    session = get_active_session(user_id)

    if not session:
        raise Exception("No active session")

    add_check_in_db(user_id, session["_id"], location, notes)

    _reset_missed(user_id)

    return {"status": "Check-in added successfully"}


def miss_check_in(user_id: str):
    """
    Increment missed check-in counter.
    """

    session = get_active_session(user_id)

    if not session:
        raise Exception("No active session")

    increment_missed_db(user_id, session["_id"])

    updated_session = get_active_session(user_id)

    return updated_session

def _reset_missed(user_id: str):
    """
    Private helper to reset missed counter.
    """
    from database.client import users_collection
    from bson import ObjectId

    users_collection.update_one(
        { "_id": ObjectId(user_id) },
        { "$set": { "sessions.check_ins_missed": 0 } }
    )


# ---------------------------
# SMS / ALERT HANDLERS
# ---------------------------

def handle_checkin_reminder(user_id: str, destination: str):
    """
    Send check-in reminder SMS.
    """

    message = "This is AltSafe. Please check-in at <weburl>."
    send_sms(destination, message)

def handle_missed_checkin(user_id: str):
    session = miss_check_in(user_id)

    if not session:
        return
    
    missed = session["check_ins_missed"]
    threshold = session["check_in_threshold"]

    if missed >= threshold:
        contact = session.get("emergency_contacts")  # Get first contact or None

        if contact:
            message = "Emergency Alert: User has missed multiple check-ins. Please check on them."
            send_sms(contact, message)