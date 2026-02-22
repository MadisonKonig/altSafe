from bson import ObjectId
from datetime import datetime
from .client import users_collection


# -----------------------------
# SESSION HELPERS
# -----------------------------

def get_active_session(user_id):
	user = users_collection.find_one(
		{"_id": ObjectId(user_id)},
		{"sessions": 1}
	)

	if not user or "sessions" not in user:
		return None
	
	for session in user["sessions"]:
		if session.get("active"):
			return session
	return None

def start_session(user_id, threshold, freq, emergency_contact):
	session_id = ObjectId()  # Generate unique session ID
	session_doc = {
		"_id": session_id,
		"active": True,
		"started_at": datetime.utcnow(),
		"ended_at": None,
		"check_ins": [],
		"check_ins_missed": 0,
		"check_in_threshold": threshold,
		"check_in_freq": freq,
		"emergency_contacts": emergency_contact
	}

	users_collection.update_one(
		{ "_id": ObjectId(user_id) },
		{ "$push": { "sessions": session_doc } }
	)

	return str(session_id)

def end_session(user_id, session_id):
	return users_collection.update_one(
		{ "_id": ObjectId(user_id), "sessions._id": ObjectId(session_id) },
		{ "$set": { "sessions.$.ended_at": datetime.utcnow(), "sessions.$.active": False } }
	)



def add_check_in(user_id, session_id, location, notes):
	return users_collection.update_one(
		{ "_id": ObjectId(user_id), "sessions._id": ObjectId(session_id) },
		{ 
			"$push": { 
				"sessions.$.check_ins": {
					"timestamp": datetime.utcnow(),
					"location": location,
					"notes": notes
				}
			},
			"$set": {
				"sessions.$.check_ins_missed": 0
			}
		}
	)

def increment_missed(user_id, session_id):
	users_collection.update_one(
		{ "_id": ObjectId(user_id), "sessions._id": ObjectId(session_id) },
		{ 
			"$inc": { 
				"sessions.$.check_ins_missed": 1
			}
		}
	)

	return get_active_session(user_id)