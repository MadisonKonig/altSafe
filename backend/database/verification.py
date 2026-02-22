from bson import ObjectId
from .client import users_collection

def set_user_verification_number(user_id, otp):
	return users_collection.update_one(
		{ "_id": ObjectId(user_id) },
		{ "$set": { "verification_number": otp } }
	)

def get_user_verification(user_id, verification_number):
	return users_collection.find_one({ 
		"_id": ObjectId(user_id), 
		"verification_number": verification_number
	})
