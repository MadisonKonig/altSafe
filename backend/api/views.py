import json
from django.shortcuts import render

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.template import Template
from django.http import JsonResponse

from database.getdata import *


# TODO: don't hardcode username & password

# database = client.get_database("sample_mflix")
# movies = database.get_collection("movies")
# # Query for a movie that has the title 'Back to the Future'
# query = { "title": "Back to the Future" }
# movie = movies.find_one(query)
# print(type(movie))
# print(movie)

# Create your views here.

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_user_data(request):
    data = get_data()
    return Response(data)

@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def delete_user_data(request):
    data = delete_data()
    return Response(data)

@api_view(['PUT'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def insert_user_data(request):
    # use the request data in insert_data() and figure out how to parse it
    data = insert_data()
    return Response(data)

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def create_user_data(request):
    # use the request data in insert_data() and figure out how to parse it
    data = create_user()
    return Response(data)

@api_view(['PUT'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def insert_user_verification_number(request):
    # use the request data in insert_data() and figure out how to parse it
    data = insert_verification_number()
    return Response(data)

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def verify_user_verification_number(request):
    # use the request data in insert_data() and figure out how to parse it
    data = verify_verification_number()
    return Response(data)

#JWT stuff
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)