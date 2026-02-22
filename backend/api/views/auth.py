from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import status

from core.auth import register_user, verify_user

@api_view(['POST'])
@permission_classes([AllowAny]) # This bypasses the User ID check, as user ID doesn't exist yet
def register(request):
    phone_number = request.data.get("phone_number")
    
    if not phone_number:
        return Response(
            {"error": "Phone number is required."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    result = register_user(phone_number)
    
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny]) # This bypasses the User ID check, as user ID doesn't exist yet
def verify(request):
	phone_number = request.data.get("phone_number")
	verification_code = request.data.get("verification_code")
	
	if not phone_number or not verification_code:
		return Response(
			{"error": "Phone number and verification code are required."}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	tokens = verify_user(phone_number, verification_code)
	
	if not tokens:
		return Response(
			{"error": "Verification failed. Please check your phone number and verification code."}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	return Response(tokens, status=status.HTTP_200_OK)