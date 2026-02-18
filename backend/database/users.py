from .client import users_collection
from bson import ObjectId

def get_users_by_id(user_id):
	user = users_collection.find_one({"_id": ObjectId(user_id)})
	if user:
		user["_id"] = str(user["_id"])
	return user