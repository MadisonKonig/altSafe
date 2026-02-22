#handles get_user and delete_user

#thin wrapper over database

from database.users import get_user_by_id, delete_data

def get_user(user_id: str) -> dict | None:
	user = get_user_by_id(user_id)
	
	if not user:
		return None
	
	if not user.get("is_verified"):
		return Exception("User is not verified")
	
	user.pop("verification_number", None)
	return user

def delete_user(user_id: str) -> None:
    delete_data(user_id)