from django.shortcuts import render
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import ReturnDocument
from requests import Response
from rest_framework.exceptions import NotFound, APIException
from rest_framework import status
from django.conf import settings

from backend.notify.services.queue import start_notify_scheduler

#TODO: See what returning error codes does - does it exit the API altogether? 

def connect_to_database():
    uri = f'mongodb+srv://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@cluster0.mma1n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
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
        return status.HTTP_200_OK
    except Exception as e:
            raise NotFound(str(e))

def create_user(name, phone_number, emergency_contact_name, emergency_contact_phone_number):
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
    return str(user.inserted_id)
    
def insert_verification_number(id, otp):
    users = connect_to_database()
    query = { "_id": ObjectId(id) }
    user = users.find_one_and_update(filter=query, update={'$set':{'verification_number':otp}}, return_document=ReturnDocument.AFTER)
    if user['verification_number'] == otp:
        return status.HTTP_200_OK
    return 500

def verify_verification_number(id, verification_number):
    try:
        users = connect_to_database()
        query = { "_id": ObjectId(id), "verification_number":verification_number }
        user = users.find_one(query)
        if verification_number == user.verification_number:
            update_is_verified(id) 
            start_session(id, "", "", 1, 2)
            start_notify_scheduler(2, user.phone_number, id)
            return status.HTTP_200_OK
    
    except APIException as e:
        return Response({"error": str(e)}, status=e.status_code)
    except Exception as e:
        return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

def end_session(id):
    users = connect_to_database()
    query = { "_id": ObjectId(id) }
    user = users.find_one_and_update(filter=query, update={'$set':{'sessions':None}}, return_document=ReturnDocument.AFTER)
    if user['sessions'] == None:
        return status.HTTP_200_OK
    return 500

def start_session(id, location, notes, check_in_threshold, check_in_freq):
    users = connect_to_database()
    query = { "_id": ObjectId(id) }
    user = users.find_one_and_update(filter=query, update={
        "$set": {  
        "sessions": {  # Set default sessions structure if inserting a new user
            "check_ins": [],
            "check_ins_missed": 0,
            "check_in_threshold": check_in_threshold,
            "check_in_freq": check_in_freq
        }
    }
    }, return_document=ReturnDocument.AFTER)
    if user['sessions']:
        check_in(id, location, notes)
        return status.HTTP_200_OK
    return 500

#TODO: the end check doesn't see if it was pushed. 
# Should count size of array and compare
def check_in(id, location, notes):
    users = connect_to_database()
    query = { "_id": ObjectId(id) }
    user = users.find_one_and_update(filter=query, update={'$push':{
                "sessions.check_ins": 
                    {
                        "location":location,
                        "notes":notes
                    }
                
        }
    }, return_document=ReturnDocument.AFTER)
    if user['sessions']:
        return status.HTTP_200_OK
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