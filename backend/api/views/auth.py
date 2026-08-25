from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import status

from core.auth import register_user, verify_user

@api_view(['POST'])
@permission_classes([AllowAny]) # This bypasses the User ID check, as user ID doesn't exist yet
@throttle_classes([AnonRateThrottle])
def register(request):
    phone_number = request.data.get("phone_number")
    result = ""
    status_code = 0
    
    if not phone_number:
        result = {"error": "Phone number is required."}
        print("Phone number required")
        status_code = status.HTTP_400_BAD_REQUEST
        
    else:
        result = register_user(phone_number)
        status_code = status.HTTP_200_OK
    
    return Response(result, status_code)

@api_view(['POST'])
@permission_classes([AllowAny]) # This bypasses the User ID check, as user ID doesn't exist yet
@throttle_classes([AnonRateThrottle])
def verify(request):
    phone_number = request.data.get("phone_number")
    verification_code = request.data.get("verification_code")

    if not phone_number or not verification_code:
       return Response(
           {"error": "Phone number and verification code are required."}, 
           status.HTTP_400_BAD_REQUEST
        )
    
    tokens = verify_user(phone_number, verification_code)
    
    if not tokens:
        return Response(
            {"error": "Verification failed. Please check your phone number and verification code."},
            status=status.HTTP_400_BAD_REQUEST
        )

    response = Response(
        {"data": phone_number, "success": True},
        status=status.HTTP_200_OK
    )
        
    response.set_cookie(
        key="access_token",
        value=tokens["access"],
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=15*60
    )
    
    return response