from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status

from database.sessions import (
	start_session,
	end_session,
	add_check_in,
	increment_missed
)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def start_session(request):
	user = request.user_id
	threshold = request.data.get("check_in_threshold")
	freq = request.data.get("check_in_freq")
	emergency_contacts = request.data.get("emergency_contacts", [])
	# emergency_contacts = request.data.get("emergency_contacts", [])

	if not threshold or not freq:
		return Response(
			{"error": "Check-in threshold and frequency are required."}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	start_session(user, threshold, freq, emergency_contacts)
	return Response(
		{"message": "Session started successfully."}, 
		status=status.HTTP_200_OK
	)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def stop_session(request):
	user = request.user_id
	end_session(user)
	return Response(
		{"message": "Session ended successfully."}, 
		status=status.HTTP_200_OK
	)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def check_in(request):
	user = request.user_id
	location = request.data.get("location")
	notes = request.data.get("notes", "")
	if not location:
		return Response(
			{"error": "Location is required for check-in."}, 
			status=status.HTTP_400_BAD_REQUEST
		)
	
	add_check_in(user, location, notes)

	return Response(
		{"message": "Check-in added successfully."}, 
		status=status.HTTP_200_OK
	)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def missed_check_in(request):
	user = request.user_id
	increment_missed(user)
	return Response(
		{"message": "Missed check-in recorded successfully."}, 
		status=status.HTTP_200_OK
	)
