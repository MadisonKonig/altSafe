from django.shortcuts import render
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import ReturnDocument
from requests import Response
from rest_framework.exceptions import NotFound, APIException
from rest_framework import status

#@TODO: See what returning error codes does - does it exit the API altogether? 

def connect_to_database():
    # TODO: don't hardcode username & password
    uri = "[REDACTED]"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    database = client.get_database("cmd-f")
    client.close()
    users = database.get_collection("users")
    return users

def get_data(id):
    users = connect_to_database()
    query = { "_id": ObjectId(id) }
    user = users.find_one(query)
    user["_id"] = str(user["_id"])
    return user

def delete_data(id):
    users = connect_to_database()
    query = { "_id": ObjectId(id) }
    try:
        users.find_one_and_delete(query)
        return 204
    except Exception as e:
            raise NotFound(str(e))

#TODO: fix end 500 error
def create_user(request):
    try:
        name = request.data.get("name")
        phone_number = request.data.get("phone number")

        if not name or not phone_number:
            raise APIException("Name and phone number are required.", code=status.HTTP_400_BAD_REQUEST)
        
        emergency_contact_name = request.data.get("emergency_contact_name")
        emergency_contact_phone_number = request.data.get("emergency_contact_phone_number")
        users = connect_to_database()
        user = users.insert_one(
        {
	        "name": name,
	        "phone_number": phone_number,
            "emergency_contacts": [
                {
                "contact_order": 1,
                "name_id": emergency_contact_name,
                "phone_number": emergency_contact_phone_number
                }
            ],
            "sessions": None,
            "is_verified": False
        })
        
        return user

    except APIException as e:
        return Response({"error": str(e)}, status=e.status_code)
    except Exception as e:
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

<<<<<<< HEAD
def insert_verification_number(id, otp):
    users = connect_to_database()
    query = { "_id": ObjectId(id) }
    user = users.find_one_and_update(filter=query, update={'$set':{'verification_number':otp}}, return_document=ReturnDocument.AFTER)
    if user['verification_number'] == otp:
        return 200
    return 500



def verify_verification_number(id, verification_number):
    users = connect_to_database()
    query = { "_id": ObjectId(id), "verification_number":verification_number }
    user = users.find_one(query)
    if user:
        update_verified(id) 
=======
def insert_verification_number(id):
    users = connect_to_database()
    query = {"phone_number":6049992857}
    ver_num = 12345
    user = users.find_one_and_update(filter=query, update={'$set':{'verification_number':ver_num}}, return_document=ReturnDocument.AFTER)
    if user['verification_number'] == ver_num:
>>>>>>> 49511203 (fixed hard coding of api calls)
        return 200
    return 500

def update_is_verified(id):
    try:
        users = connect_to_database()
        query = { "_id": ObjectId(id) }
        user = users.find_one_and_update(filter=query, update=({'$set':{'is_verified':True}}))
        user["_id"] = str(user["_id"])

        return user
    
    except APIException as e:
        return Response({"error": str(e)}, status=e.status_code)
    except Exception as e:
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# TODO get verification number from request. 
# We need to get the user, check if the numbers match. 
# True = change db val. False = return error
def verify_verification_number(request):
    try:
        id = request.data.get("id")
        verification_number = request.data.get("verification_number")
        users = connect_to_database()
        query = { "_id": ObjectId(id) }
        user = users.find_one(query)
        print(user)
        if verification_number == user.verification_number:
            # update_is_verified(id)
            return 200
    
    except APIException as e:
        return Response({"error": str(e)}, status=e.status_code)
    except Exception as e:
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def end_session():
    users = connect_to_database()
    phone_number = 6049992857
    query = {"phone_number":phone_number}
    user = users.find_one_and_update(filter=query, update={'$set':{'sessions':None}}, return_document=ReturnDocument.AFTER)
    if user['sessions'] == None:
        return 200
    return 500

def start_session():
    location = "loc"
    notes = 'notes'
    check_in_threshold = 3
    check_in_freq = 300
    users = connect_to_database()
    phone_number = 6039992852
    query = {"phone_number":phone_number}
    user = users.find_one_and_update(filter=query, update={
        "$set": {  
        "sessions": {  # Set default sessions structure if inserting a new user
            "check_ins": [],
            "check_ins_missed": 0,
            "check_in_threshold": 3,
            "check_in_freq": 300
        }
    }
    }, return_document=ReturnDocument.AFTER)
    print(user)
    if user['sessions']:
        check_in()
        return 200
    return 500

#TODO: the end check doesn't see if it was pushed. 
# Should count size of array and compare
def check_in():
    location = "loccc"
    notes = 'notesss'
    users = connect_to_database()
    phone_number = 6039992852
    query = {"phone_number":phone_number}
    user = users.find_one_and_update(filter=query, update={'$push':{
                "sessions.check_ins": 
                    {
                        "location":location,
                        "notes":notes
                    }
                
        }
    }, return_document=ReturnDocument.AFTER)
    if user['sessions']:
        return 200
    return 500

#TODO: end check is pointless. but mvp babbby
def miss_check_in(id):
    users = connect_to_database()
    query = { "_id": ObjectId(id) }
    try:
        user = users.find_one_and_update(filter=query, update={'$inc':
                { "sessions.check_ins_missed": 1 }
            }, return_document=ReturnDocument.AFTER)
        
        return user
    except Exception as e:
            raise NotFound(str(e))