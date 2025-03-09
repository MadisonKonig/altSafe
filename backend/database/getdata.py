from django.shortcuts import render

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi



def connect_to_database():
    # TODO: don't hardcode username & password
    uri = "[REDACTED]"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    database = client.get_database("cmd-f")
    client.close()
    users = database.get_collection("users")
    return users

def get_data():
    users = connect_to_database()
    # Query for a movie that has the title 'Back to the Future'
    query = { "phone_number": 6049992837 }
    user = users.find_one(query)
    user["_id"] = str(user["_id"])
    return user

def delete_data():
    users = connect_to_database()
    users.find_one_and_delete
    return 204

def insert_data():
    users = connect_to_database()
    print('test')
    # print(data)
    query = {"phone_number":6049992837}
    user = users.find_one_and_update(filter=query, update={})
    return 500

def insert_session():
    users = connect_to_database()
    print('test')
    query = {"phone_number":6049992837} #{'$inc': {'x': 3}}
    user = users.find_one_and_update(filter=query, update=({'$set':{'is_verified':True}}))
    user["_id"] = str(user["_id"])
    return user



# @api_view(('GET',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def get_data(request):
    
#     return Response(user)

# #
# @api_view(('INSERT',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def insert_data(request):
#     uri = "[REDACTED]"

#     # Create a new client and connect to the server
#     client = MongoClient(uri, server_api=ServerApi('1'))
#     [...]
#     database = client.get_database("cmd-f")
#     users = database.get_collection("users")
#     # Query for a movie that has the title 'Back to the Future'
#     query = { "phone_number": 6049992837 }
#     user = users.find_one(query)
#     if user:
#         user["_id"] = str(user["_id"])
#     return Response(user)

# @api_view(('DELETE',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def delete_data(request):
#     uri = "[REDACTED]"

#     # Create a new client and connect to the server
#     client = MongoClient(uri, server_api=ServerApi('1'))
#     [...]
#     database = client.get_database("cmd-f")
#     users = database.get_collection("users")
#     # Query for a movie that has the title 'Back to the Future'
#     query = { "phone_number": 6049992837 }
#     user = users.find_one(query)
#     if user:
#         user["_id"] = str(user["_id"])
#     return Response(user)