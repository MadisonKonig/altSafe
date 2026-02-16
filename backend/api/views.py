
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from notify.services.sms import send_verification
import secrets

from database.getdata import *

# TODO: get data from body and replace hardcoding
# TODO: need to invoke method from notify to send the verification text message
# returns: JWT token
@api_view(['POST'])
@permission_classes([AllowAny]) # This bypasses the User ID check, as user ID doesn't exist yet
def register(request):
    phone_number = request.data.get("phone_number")
    if not phone_number:
        raise APIException("phone number are required.", code=status.HTTP_400_BAD_REQUEST)
    
    users = connect_to_database()
    creation_code = f"{secrets.randbelow(100000):05d}"
    if check_user_in(users, phone_number):
        #update verification code
        user = update_verification_number(users, phone_number, creation_code)
    else:
        user = create_user(users, phone_number, creation_code)
    send_verification(phone_number, creation_code)
    return Response(user)

# TODO get verification number from request. 
# We need to get the user, check if the numbers match. 
# True = change db val. False = return error
@api_view(['PUT'])  # naming
#TODO Delete later, bypassing for testing
@permission_classes([AllowAny])
def verify_user_verification_number(request):
    users = connect_to_database()
    user = request.user
    data = verify_verification_number(users, user.id, user.verification_number)
    return Response(data)


# TODO: don't hardcode username & password

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_user_data(request):
    user = request.user
    # print(user)
    return Response(get_data(user.id))

@api_view(['DELETE'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def delete_user_data(request):
    user = request.user
    data = delete_data(user.id)
    return Response(data)

@api_view(['PUT'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def insert_user_data(request):
    phone_number = request.phone_number
    # use the request data in insert_data() and figure out how to parse it
    data = insert_data(phone_number)
    return Response(data)

# TODO: get data from body and replace hardcoding
# TODO: need to invoke method from notify to send the verification text message
# returns: JWT token
@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
@permission_classes([AllowAny]) # This bypasses the User ID check, as user ID doesn't exist yet
def create_user_data(request):
    name = request.data.get("name")
    phone_number = request.data.get("phone_number")
    if not name or not phone_number:
        raise APIException("Name and phone number are required.", code=status.HTTP_400_BAD_REQUEST)
    
    emergency_contact_name = request.data.get("emergency_contact_name")
    emergency_contact_phone_number = request.data.get("emergency_contact_phone_number")
    if not emergency_contact_name or not emergency_contact_phone_number:
        raise APIException("Emergency name and phone number are required.", code=status.HTTP_400_BAD_REQUEST)
    
    user = create_user(name, phone_number, emergency_contact_name, emergency_contact_phone_number)
    send_verification(user, phone_number)
    return Response(user)

# @api_view(['PUT'])
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))

# TODO we actually don't need this because we will call the db method from the notify app.
# def insert_user_verification_number(request):
#     user = request.user
#     # use the request data in insert_data() and figure out how to parse it
#     data = insert_verification_number(user.id)
#     return Response(data)




@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def end_user_session(request):
    user = request.user
    data = end_session(user.id)
    return Response(data)

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def start_user_session(request):
    # use the request data in insert_data() and figure out how to parse it
    user = request.user
    data = start_session(
        user.id, 
        user.location, 
        user.notes, 
        user.check_in_threshold, 
        user.check_in_freq
    )
    return Response(data)

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def check_user_in(request):
    # use the request data in insert_data() and figure out how to parse it
    user = request.user
    # print("this is the location: ", request.data.get("location"))
    # print(user.location)
    data = check_in(user.id, user.location, user.notes)
    return Response(data)

@api_view(['POST'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def miss_user_check_in(request):
    # use the request data in insert_data() and figure out how to parse it
    user = request.user
    data = miss_check_in(user.id)
    return Response(data)

#JWT stuff
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services.jwt import create_jwt

@api_view(['GET'])
@permission_classes([AllowAny])
# THIS IS SOLELY FOR POSTMAN USAGE
def createDummyJwt(request):
    # Secret key used to encode and decode JWTs (same as the one you used in settings.py for Simple JWT)
    SECRET_KEY = settings.SECRET_KEY

    # Generate the JWT token
    token = create_jwt("67cd77ec65f13195e417028d")

    # Print the token
    return Response(token)
    
class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
