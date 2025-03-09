from django.shortcuts import render
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import ReturnDocument
from rest_framework.exceptions import NotFound

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
    
# def insert_data():
#     users = connect_to_database()
#     print('test')
#     # print(data)
#     query = {"phone_number":6049992837}
#     user = users.find_one_and_update(filter=query, update={})
#     return 500

def update_verified(id):
    users = connect_to_database()
    print('test')
    query = { "_id": ObjectId(id) }
    user = users.find_one_and_update(filter=query, update=({'$set':{'is_verified':True}}))
    user["_id"] = str(user["_id"])
    return user

def create_user():
    users = connect_to_database()
    user = users.insert_one(
        {
	        "name":"Dilbert",
	        "phone_number":6049992845,
            "emergency_contacts": [
                {
                "contact_order": 1,
                "name_id": "The Kid",
                "phone_number": 6047782938
                }
            ],
            "sessions": {
                "check_ins": [
                    {
                        "location":"coords",
                        "notes":"plate number: xyz"
                    }
                ],
                "check_ins_missed": 0,
                "check_in_threshold": 3,
                "check_in_freq": 300
            },
            "is_verified": False
        })
    #user.inserted_id is the newly made user
    if user.acknowledged:
        return user
    return 500


# def insert_verification_number():
#     users = connect_to_database()
#     print('test')
#     # print(data)
#     query = {"phone_number":6049992857}
#     ver_num = 12345
#     user = users.find_one_and_update(filter=query, update={'$set':{'verification_number':ver_num}}, return_document=ReturnDocument.AFTER)
#     if user['verification_number'] == ver_num:
#         return 200
#     return 500



def verify_verification_number(id, verification_number):
    users = connect_to_database()
    query = { "_id": ObjectId(id), "verification_number":verification_number }
    user = users.find_one(query)
    if user:
        update_verified(id)
        return 200
    return 500

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
    phone_number = 6049992857
    query = {"phone_number":phone_number}
    user = users.find_one_and_update(filter=query, update={'$set':{'sessions':
            {
                "check_ins": [
                    {
                        "location":location,
                        "notes":notes
                    }
                ],
                "check_ins_missed": 0,
                "check_in_threshold": check_in_threshold,
                "check_in_freq": check_in_freq
            }
        }
    }, return_document=ReturnDocument.AFTER)
    if user['sessions']:
        return 200
    return 500