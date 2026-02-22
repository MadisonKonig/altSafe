from .client import users_collection
from bson import ObjectId

#might not need
def get_user_by_id(user_id):
	user = users_collection.find_one({"_id": ObjectId(user_id)})
	if user:
		user["_id"] = str(user["_id"])
	return user

def get_user_by_phone_number(phone_number):
	return users_collection.find_one({"phone_number": phone_number})

def create_user(phone_number, code):
    result = users_collection.insert_one(
    {
        "phone_number": phone_number,
        "verification_number": code,
        "sessions": None,
        "is_verified": False
    })
    return str(result.inserted_id)

def delete_data(user_id):
    users_collection.delete_one({"_id": ObjectId(user_id)})
    
def set_verification_code(phone_number, code):
    return users_collection.update_one(
        {"phone_number": phone_number},
        {"$set": {"verification_number": code}}
    )

def update_is_verified(phone_number):
   return users_collection.update_one(
		{"phone_number": phone_number},
		{"$set": {"is_verified": True}}
	)
