from bson import ObjectId
from datetime import datetime, timezone
from .client import users_collection, sessions_collection


# -----------------------------
# SESSION HELPERS
# -----------------------------

def get_active_session(user_id):
    return users_collection.find_one(
        {"_id": ObjectId(user_id)},
        {"has_active_session": True}
    )

def get_session(user_id, session_id):
    return sessions_collection.find_one({
        "_id": ObjectId(session_id), 
        "user_id": ObjectId(user_id) 
    })


def start_session(user_id, threshold, freq, emergency_contact):
    session_id = ObjectId()  # Generate unique session ID
    session_doc = {
        "_id": session_id,
        "user_id": ObjectId(user_id),
        "active": True,
        "started_at": datetime.now(timezone.utc),
        "ended_at": None,
        "check_ins": [],
        "check_ins_missed": 0,
        "check_in_threshold": threshold,
        "check_in_freq": freq,
        "emergency_contacts": emergency_contact
    }

    sessions_collection.insert_one(session_doc)

    users_collection.update_one(
        { "_id": ObjectId(user_id) },
        { "$set": { "has_active_session": True } }
    )

    return str(session_id)

def end_session(user_id, session_id):
    users_collection.update_one(
        {"_id": ObjectId(session_id)}, 
        {"$set":{"has_active_session":False}}
    )

    return sessions_collection.update_one(
        {   
            "_id": ObjectId(session_id), 
            "user_id": ObjectId(user_id),
            "active": True 
        },
        { 
            "$set": { 
                "ended_at": datetime.now(timezone.utc), 
                "active": False
            }
        }
    )

def add_check_in(user_id, session_id, location, notes):
    return sessions_collection.update_one(
        { 
            "_id": ObjectId(session_id), 
            "user_id": ObjectId(user_id),
            "active": True
        },
        { 
            "$push": { 
                "check_ins": {
                    "timestamp": datetime.now(timezone.utc),
                    "location": location,
                    "notes": notes
                }
            },
            "$set": {
                "check_ins_missed": 0
            }
        }
    )

def increment_missed(user_id, session_id):
    result = sessions_collection.update_one(
        { 
            "_id": ObjectId(session_id), 
            "user_id": ObjectId(user_id),
            "active": True
        },
        { 
            "$inc": { 
                "check_ins_missed": 1
            }
        }
    )

    return result