
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

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
    user = request.user
    return Response(get_data(user.id))

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
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services.jwt import create_jwt

# THIS IS SOLELY FOR POSTMAN USAGE
def createDummyJwt():
    # Secret key used to encode and decode JWTs (same as the one you used in settings.py for Simple JWT)
    SECRET_KEY = settings.SECRET_KEY

    # Generate the JWT token
    token = create_jwt("67cd77ec65f13195e417028d")

    # Print the token
    return token
    
class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)