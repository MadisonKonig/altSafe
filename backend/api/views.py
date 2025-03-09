from django.shortcuts import render

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# TODO: don't hardcode username & password
uri = "[REDACTED]"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Create your views here.

def homeview(request):
    database = client.get_database("sample_mflix")
    movies = database.get_collection("movies")
    # Query for a movie that has the title 'Back to the Future'
    query = { "title": "Back to the Future" }
    movie = movies.find_one(query)
    return render(
        request,
        'index.html',
        {
            'movie': movie
        }
    )


# def index(request):
#     collection_city = db['city']
#     collection_languages = db['languages']

#     cities = list(collection_city.find())
#     languages = list(collection_languages.find())
#     dests=Destination.objects.all()
#     return render(
#         request,
#         'index.html', 
#         {
            
#         }
#     )
