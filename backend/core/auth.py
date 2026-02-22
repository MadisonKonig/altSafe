import secrets
from core.jwt import create_tokens
from database.users import create_user, update_is_verified, get_user_by_phone_number, set_verification_code
from services.sms import send_sms

# should handle register and verification of users
# uses database.users, database.verification, and services.sms

def register_user(phone_number: str):
	code = f"{secrets.randbelow(100000):05d}"
	user = get_user_by_phone_number(phone_number)

	if user:
		set_verification_code(phone_number, code)
		user_id = str(user["_id"])
	else:
		user_id = create_user(phone_number, code)
	
	send_sms(phone_number, f"Your verification code is: {code}")
	return {"user_id": user_id}

def verify_user(phone_number, verification_number):
	user = get_user_by_phone_number(phone_number)
	if not user:
		return None
	
	# this needs to check the stored verification number against the one provided, and only verify if they match. 
	# This is to prevent someone from just calling the verify endpoint with any code and verifying themselves.
	if user["verification_number"] != verification_number:
		return None
	
	update_is_verified(phone_number)
	#clear_verification_code(phone_number) 
	# this is optional, but it can help prevent confusion if the user tries to verify again with the same code.

	tokens = create_tokens(str(user["_id"]))
	# start_session(user_id, threshold=3, freq=2)
	# start_notify_scheduler(freq=2, phone_number=user["phone_number"], user_id=user_id)
	return tokens