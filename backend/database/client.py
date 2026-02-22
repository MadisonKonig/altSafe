from pymongo import MongoClient
from django.conf import settings

client = MongoClient(
    f"mongodb+srv://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@cluster0.mma1n.mongodb.net/?retryWrites=true&w=majority"
)

db = client.get_database("cmd-f")
users_collection = db.get_collection("users")