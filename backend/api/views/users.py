from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from database.users import get_user_by_id, delete_data

@api_view(['GET'])
def get_user(request):
	user = request.user
	data = get_user_by_id(user.id)
	if not data:
		return Response(
			{"error": "User not found."}, 
			status=status.HTTP_404_NOT_FOUND
		)
	return Response(data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_user_data(request):
	user = request.user
	delete_data(user.id)
	return Response(
		{"message": "User data deleted successfully."}, 
		status=status.HTTP_200_OK
	)

